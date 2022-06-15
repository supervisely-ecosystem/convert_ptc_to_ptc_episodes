import supervisely as sly
from supervisely import logger

import src.sly_functions as f
import src.sly_globals as g

from collections import OrderedDict

from supervisely.video_annotation.key_id_map import KeyIdMap
from supervisely.video_annotation.frame_collection import FrameCollection
from supervisely.video_annotation.video_figure import VideoFigure
from supervisely.video_annotation.video_tag_collection import VideoTagCollection
from supervisely.pointcloud_annotation.pointcloud_object_collection import PointcloudObjectCollection

from supervisely.geometry.cuboid_3d import Cuboid3d, Vector3d
import numpy as np

logger.info("Application has been started")
progress = sly.Progress('Processing annotations', sum(ds.items_count for ds in g.project_datasets))
ds_name_to_ann = {}
ds_names_to_frames = {}
for dataset in g.project_datasets:
    pointclouds = g.api.pointcloud.get_list(dataset.id)
    names_to_ptcs = {ptc.name : ptc.id for ptc in pointclouds}

    names_to_ptcs = OrderedDict(names_to_ptcs.items())
    names_to_ptcs = OrderedDict(sorted(names_to_ptcs.items(), key=lambda t: t[0]))
    frames_to_ptcs = {i: v for i, v in enumerate(names_to_ptcs.values())}
    ptcs_to_names = {v: k for k, v in names_to_ptcs.items()}
    frames_to_ptc_names = {k: ptcs_to_names[v] for k, v in frames_to_ptcs.items()}
    ds_names_to_frames[dataset.name] = frames_to_ptc_names

    key_to_objects = {}
    ptc_key_id = KeyIdMap()

    ann_json = g.api.pointcloud_episode.annotation.download(dataset.id)
    ann = sly.PointcloudEpisodeAnnotation.from_json(ann_json, g.project_meta, ptc_key_id)
    if dataset.name == "KITTI360":
        ds_name_to_ann[dataset.name] = ann
        continue
    objects_collection = ann.objects

    new_frames = []
    for frame_ind, frame in enumerate(ann.frames):
        new_figs = []
        for fig in frame.figures:
            if not isinstance(fig.geometry, Cuboid3d):
                continue
            rotation = fig.geometry.rotation
            z = rotation.z + np.pi
            if z > np.pi:
                z = -np.pi + rotation.z
            rotation = Vector3d(0, 0, z)
            new_cuboid = Cuboid3d(fig.geometry.position, rotation, fig.geometry.dimensions)
            fig._set_geometry_inplace(new_cuboid)
            new_figs.append(fig)

        new_frames.append(sly.Frame(frame_ind, new_figs))
    ann = sly.PointcloudEpisodeAnnotation(
        frames_count=len(new_frames),
        objects=objects_collection, 
        frames=FrameCollection(new_frames), 
        tags=VideoTagCollection([])
    )
    ds_name_to_ann[dataset.name] = ann

project_names = [x.name for x in g.api.project.get_list(g.workspace_id)]
new_project_name = sly._utils.generate_free_name(used_names=project_names, possible_name=g.new_project_name)

progress = sly.Progress('Cloning point clouds', 1)
clone_task_id = g.api.project.clone_advanced(g.project_id, g.workspace_id, new_project_name, with_annotations=False)
g.api.task.wait(clone_task_id, g.api.task.Status('finished'))

progress.iter_done_report()

new_project = g.api.project.get_info_by_name(g.workspace_id, new_project_name)
new_project_id = new_project.id

new_datasets = g.api.dataset.get_list(new_project_id)
progress = sly.Progress('Uploading converted annotations', len(new_datasets))
for ds_ind, dataset in enumerate(new_datasets):
    frames_to_ptc_names = ds_names_to_frames[dataset.name]
    pointclouds = g.api.pointcloud.get_list(dataset.id)
    names_to_ptcs = {ptc.name : ptc.id for ptc in pointclouds}
    frames_to_ptcs = {k: names_to_ptcs[v] for k, v in frames_to_ptc_names.items()}

    g.api.pointcloud_episode.annotation.append(dataset.id,
                                                ds_name_to_ann[dataset.name],
                                                frames_to_ptcs,
                                                KeyIdMap())
    progress.iter_done_report()

g.api.task.set_output_project(g.task_id, new_project_id, new_project_name)
f.shutdown_app()
