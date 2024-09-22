from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session
from datetime import datetime

from ..models.person import RefreshToken
from ..core.db import get_session
from ..schemas.auth_schema import (
    ResponseSchema,
    RegisterSchema,
    LoginSchema,
    ForgotPasswordSchema,
)
from ..services.auth_service import AuthService
from ..repositories.auth import CurrentRefreshToken

router = APIRouter()


@router.post(
    "/register", response_model=ResponseSchema, response_model_exclude_none=True
)
async def register(
    register_body: RegisterSchema,
    response: Response,
    session: Session = Depends(get_session),
):
    access_token, access_expires, refresh_token, refresh_expires = (
        await AuthService.register_service(session=session, register=register_body)
    )

    response.set_cookie(
        key="access_token", value=access_token, httponly=True, expires=access_expires
    )
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, expires=refresh_expires
    )

    return ResponseSchema(detail="Successful create")


@router.post("/login", response_model=ResponseSchema)
async def login(
    login_body: LoginSchema, response: Response, session: Session = Depends(get_session)
):
    access_token, access_expires, refresh_token, refresh_expires = (
        await AuthService.login_service(session=session, login=login_body)
    )

    response.set_cookie(
        key="access_token", value=access_token, httponly=True, expires=access_expires
    )
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, expires=refresh_expires
    )

    return ResponseSchema(detail="Successful login")


@router.get("/refresh", response_model=ResponseSchema)
async def refres_access_token(
    response: Response, refresh_token: RefreshToken = CurrentRefreshToken
):
    access_token, access_expires = await AuthService.refresh_access_token(
        refresh_token=refresh_token
    )
    response.set_cookie(
        key="access_token", value=access_token, httponly=True, expires=access_expires
    )

    return ResponseSchema(detail="Successfully refreshed")


@router.post("/forgot-password", status_code=status.HTTP_201_CREATED)
async def forgot_password(
    forgot_body: ForgotPasswordSchema,
    session: Session = Depends(get_session),
):
    await AuthService.fogot_password_service(
        session=session, forgotPassword=forgot_body
    )

    return
