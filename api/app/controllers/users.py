from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, APIKeyCookie
from sqlmodel import Session

from ..repositories.auth import get_auth_user
from ..models.person import User

router = APIRouter()


@router.get("")
async def register_user(user: User = Depends(get_auth_user)):
    return user
