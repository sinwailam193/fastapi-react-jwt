import time
from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..core.db import get_session
from ..repositories.person import PersonRepo
from ..repositories.auth import JWTRepo

router = APIRouter()


@router.get("")
async def register_user(session: Session = Depends(get_session)):
    person = await PersonRepo.find_by_name(
        name="Sin Wai",
        session=session,
    )
    people = await PersonRepo.get_all(session=session)
    return "hello world"
