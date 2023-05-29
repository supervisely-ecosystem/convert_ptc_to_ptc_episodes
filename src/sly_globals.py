import os
from pathlib import Path

from fastapi import FastAPI
from supervisely.sly_logger import logger

import supervisely as sly
from supervisely.app.fastapi import create

app_root_directory = str(Path(__file__).parent.absolute().parents[0])
logger.info(f"App root directory: {app_root_directory}")

# from dotenv import load_dotenv
# if sly.is_development():
#     load_dotenv("debug.env")
#     load_dotenv(os.path.expanduser("~/supervisely.env"))

team_id = int(os.environ["TEAM_ID"])
project_id = int(os.environ["PROJECT_ID"])
workspace_id = int(os.environ["WORKSPCE_ID"])
task_id = int(os.environ["TASK_ID"])

api = sly.Api.from_env()
app = FastAPI()
sly_app = create()

project_info = api.project.get_info_by_id(project_id)
project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
project_datasets = api.dataset.get_list(project_id)

new_project_name = f"{project_info.name}_episodes"

app.mount("/sly", sly_app)
