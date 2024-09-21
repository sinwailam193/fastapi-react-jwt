from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session
from datetime import datetime

from ..core.db import get_session
from ..core.config import settings
from ..schemas.auth_schema import (
    ResponseSchema,
    RegisterSchema,
    LoginSchema,
    ForgotPasswordSchema,
)
from ..services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register", response_model=ResponseSchema, response_model_exclude_none=True
)
async def register(
    register_body: RegisterSchema,
    response: Response,
    session: Session = Depends(get_session),
):
    token, expires = await AuthService.register_service(
        session=session, register=register_body
    )

    response.set_cookie(key="access_token", value=token, httponly=True, expires=expires)

    return ResponseSchema(detail="Successful create")


@router.post("/login", response_model=ResponseSchema)
async def login(
    login_body: LoginSchema, response: Response, session: Session = Depends(get_session)
):
    token, expires = await AuthService.login_service(session=session, login=login_body)

    response.set_cookie(key="access_token", value=token, httponly=True, expires=expires)

    return ResponseSchema(detail="Successful login")


@router.post("/forgot-password", status_code=status.HTTP_201_CREATED)
async def forgot_password(
    forgot_body: ForgotPasswordSchema,
    session: Session = Depends(get_session),
):
    await AuthService.fogot_password_service(
        session=session, forgotPassword=forgot_body
    )

    return
