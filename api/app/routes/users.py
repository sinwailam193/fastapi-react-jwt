from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.core.db import db_init
from app.services.user import get_user_by_username, create_user

router = APIRouter()


@router.post("")
def register_user(user: UserCreate, db: Session = Depends(db_init)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return create_user(db, user)
