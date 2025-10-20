from app.core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api_v1 import api_v1
import os


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(api_v1, prefix=API_PREFIX)

    os.makedirs("downloads", exist_ok=True)

    application.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")
    return application


app = get_application()
