from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..core.db import get_session
from ..repositories.person import PersonRepo
from ..repositories.auth import JWTRepo
from ..services.user_service import UserService

router = APIRouter()


@router.get("")
async def register_user(session: Session = Depends(get_session)):
    # person = await PersonRepo.find_by_name(
    #     name="Sin Wai",
    #     session=session,
    # )
    # people = await PersonRepo.get_all(session=session)
    user = await UserService.get_user_profile(session=session, user_id=1)
    return user
