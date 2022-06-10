import supervisely as sly


def shutdown_app():
    try:
        sly.app.fastapi.shutdown()
    except Exception:
        sly.logger.info("Application shutdown successfully")
