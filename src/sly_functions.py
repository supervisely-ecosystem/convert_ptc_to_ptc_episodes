import supervisely as sly
import sly_globals as g
from supervisely.api.module_api import ApiField


def shutdown_app():
    try:
        sly.app.fastapi.shutdown()
    except KeyboardInterrupt:
        sly.logger.info("Application shutdown successfully")


def prepare_info_lists(pcd_infos):
    names = []
    hashes = []
    metas = []
    frame_nums = [n for n in range(len(pcd_infos))]
    for info in pcd_infos:
        names.append(info.name)
        hashes.append(info.hash)
        metas.append(info.meta)
    combined_info = zip(names, hashes, metas)
    sorted_info = sorted(combined_info, key=lambda x: x[0])
    names, hashes, metas = zip(*sorted_info)
    for meta, num in zip(metas, frame_nums):
        meta["frame"] = num

    return names, hashes, metas


def prepare_related_images(pcd_infos, new_pcd_infos):
    prepared_images = []
    new_pcd_name_id_dict = {new_pcd_info.name: new_pcd_info.id for new_pcd_info in new_pcd_infos}
    for pcd_info in pcd_infos:
        rel_image = g.api.pointcloud.get_list_related_images(id=pcd_info.id)
        if len(rel_image) == 0:
            sly.logger.warn(f"{pcd_info.name} have no hash. Item will be skipped.")
            continue
        else:
            rel_image = rel_image[0]
            related_id = new_pcd_name_id_dict[pcd_info.name]
            prepared_images.append(
                {
                    ApiField.ENTITY_ID: related_id,
                    ApiField.NAME: rel_image[ApiField.NAME],
                    ApiField.HASH: rel_image[ApiField.HASH],
                    ApiField.META: rel_image[ApiField.META],
                }
            )
    return prepared_images
