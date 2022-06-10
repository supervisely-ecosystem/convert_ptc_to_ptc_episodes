import os
from pathlib import Path

from fastapi import FastAPI
from supervisely.sly_logger import logger
from starlette.staticfiles import StaticFiles

import supervisely
from supervisely.app.fastapi import create, Jinja2Templates

app_root_directory = str(Path(__file__).parent.absolute().parents[0])
logger.info(f"App root directory: {app_root_directory}")

# @TODO: for debug
# from dotenv import load_dotenv
# debug_env_path = os.path.join(app_root_directory, "debug.env")
# secret_debug_env_path = os.path.join(app_root_directory, "secret_debug.env")
# load_dotenv(debug_env_path)
# load_dotenv(secret_debug_env_path, override=True)

team_id = int(os.environ['context.teamId'])
project_id = int(os.environ['modal.state.slyProjectId'])
workspace_id = int(os.environ['context.workspaceId'])

api = supervisely.Api.from_env()
app = FastAPI()
sly_app = create()

project_info = api.project.get_info_by_id(project_id)
project_meta = supervisely.ProjectMeta.from_json(api.project.get_meta(project_id))
project_datasets = api.dataset.get_list(project_id)

new_project_name = f"{project_info.name}_episodes"

app.mount("/sly", sly_app)


