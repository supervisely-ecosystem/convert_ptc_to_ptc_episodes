import supervisely as sly
from supervisely import logger

import src.sly_functions as f
import src.sly_globals as g

from collections import OrderedDict

from supervisely.video_annotation.key_id_map import KeyIdMap
from supervisely.video_annotation.frame_collection import FrameCollection
from supervisely.pointcloud_annotation.pointcloud_episode_annotation import (
    PointcloudEpisodeTagCollection,
)
from supervisely.pointcloud_annotation.pointcloud_object_collection import (
    PointcloudObjectCollection,
)

from supervisely.api.project_api import ProjectApi

logger.info("Application has been started")
progress = sly.Progress("Processing annotations", sum(ds.items_count for ds in g.project_datasets))
ds_names_to_anns = {}
ds_names_to_frames = {}
for dataset in g.project_datasets:
    pointclouds = g.api.pointcloud.get_list(dataset.id)
    names_to_ptcs = {ptc.name: ptc.id for ptc in pointclouds}

    names_to_ptcs = OrderedDict(names_to_ptcs.items())
    names_to_ptcs = OrderedDict(sorted(names_to_ptcs.items(), key=lambda t: t[0]))
    frames_to_ptcs = {i: v for i, v in enumerate(names_to_ptcs.values())}
    ptcs_to_frames = {v: k for k, v in frames_to_ptcs.items()}
    pointcloud_ids = list(names_to_ptcs.values())

    frames = []
    key_to_objects = {}
    ptc_key_id = KeyIdMap()
    for ptc_ind, ptc_id in enumerate(pointcloud_ids):
        ann_json = g.api.pointcloud.annotation.download(ptc_id)
        ann = sly.PointcloudAnnotation.from_json(ann_json, g.project_meta, ptc_key_id)
        for ann_object in ann.objects:
            if ann_object.key() not in key_to_objects.keys():
                key_to_objects[ann_object.key()] = ann_object
        frames.append(sly.Frame(ptcs_to_frames[ptc_id], ann.figures))
        progress.iter_done_report()

    objects_collection = PointcloudObjectCollection(key_to_objects.values())
    annotation = sly.PointcloudEpisodeAnnotation(
        frames_count=len(frames),
        objects=objects_collection,
        frames=FrameCollection(frames),
        tags=PointcloudEpisodeTagCollection([]),
    )

    ds_names_to_anns[dataset.name] = annotation

    ptcs_to_names = {v: k for k, v in names_to_ptcs.items()}
    frames_to_ptc_names = {k: ptcs_to_names[v] for k, v in frames_to_ptcs.items()}
    ds_names_to_frames[dataset.name] = frames_to_ptc_names

project_names = [x.name for x in g.api.project.get_list(g.workspace_id)]
new_project_name = sly._utils.generate_free_name(
    used_names=project_names, possible_name=g.new_project_name
)

new_project = g.api.project.create(
    g.workspace_id,
    new_project_name,
    type=sly.ProjectType.POINT_CLOUD_EPISODES,
    change_name_if_conflict=True,
)
new_project_id = new_project.id

project_meta_update = g.project_meta.to_json()
project_meta_update = g.project_meta.clone(project_type=sly.ProjectType.POINT_CLOUD_EPISODES.value)
g.api.project.update_meta(new_project_id, project_meta_update)


progress = sly.Progress(
    message=f"Converting point clouds dataset [{dataset.name}] into episode",
    total_cnt=len(g.project_datasets),
)
for i, dataset in zip(range(len(g.project_datasets)), g.project_datasets):
    dataset_name = f"episode_{i}"
    new_dataset_info = g.api.dataset.create(new_project_id, dataset_name)
    pcd_infos = g.api.pointcloud.get_list(dataset_id=dataset.id)

    names, hashes, metas = f.prepare_info_lists(pcd_infos)
    new_pcd_infos = g.api.pointcloud_episode.upload_hashes(
        new_dataset_info.id, names, hashes, metas
    )
    prepared_images = f.prepare_related_images(pcd_infos, new_pcd_infos)
    g.api.pointcloud_episode.add_related_images(prepared_images)
    ds_names_to_frames[dataset_name] = ds_names_to_frames.pop(dataset.name)
    ds_names_to_anns[dataset_name] = ds_names_to_anns.pop(dataset.name)
    progress.iter_done_report()

new_datasets = g.api.dataset.get_list(new_project_id)
progress = sly.Progress("Uploading converted annotations", len(new_datasets))
for dataset in new_datasets:
    frames_to_ptc_names = ds_names_to_frames[dataset.name]
    pointclouds = g.api.pointcloud_episode.get_list(dataset.id)
    names_to_ptcs = {ptc.name: ptc.id for ptc in pointclouds}
    frames_to_ptcs = {k: names_to_ptcs[v] for k, v in frames_to_ptc_names.items()}

    annotation = ds_names_to_anns[dataset.name]
    g.api.pointcloud_episode.annotation.append(dataset.id, annotation, frames_to_ptcs, KeyIdMap())
    progress.iter_done_report()

g.api.task.set_output_project(g.task_id, new_project_id, new_project_name)
f.shutdown_app()
