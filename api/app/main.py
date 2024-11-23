import uvicorn
from fastapi import FastAPI

from .core.config import settings, Settings
from .controllers.main import api_router


def create_app(settings: Settings):
    app = FastAPI()

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


api = create_app(settings=settings)
