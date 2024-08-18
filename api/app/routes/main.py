from fastapi import APIRouter

from app.routes import users, bands

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(bands.router, prefix="/bands", tags=["bands"])
