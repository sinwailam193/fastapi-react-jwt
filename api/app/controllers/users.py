from fastapi import APIRouter

from ..repositories.auth import CurrentUser
from ..models.person import User

router = APIRouter()


@router.get("")
async def register_user(user=CurrentUser):

    return user
