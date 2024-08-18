from fastapi import FastAPI
from contextlib import asynccontextmanager

from .core.config import settings
from .core.db import init_db
from .routes.main import api_router
import app.models.album


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)
