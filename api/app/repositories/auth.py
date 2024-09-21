import time
from fastapi import HTTPException, status, Depends, Response
from fastapi.security import APIKeyCookie
from sqlmodel import Session
from datetime import timedelta, datetime, timezone
from jose.jwt import encode, decode
from jose.exceptions import ExpiredSignatureError, JWTError

from ..core.config import settings
from ..core.db import get_session
from ..services.user_service import UserService
from ..repositories.users import UserRepo


class JWTRepo:
    def __init__(self, data: dict = {}, token: str = None) -> None:
        self.data = data
        self.token = token

    def generate_token(self, expires_delta: timedelta | None = None):
        to_encode = self.data.copy()

        if expires_delta:
            expires = datetime.now(timezone.utc) + expires_delta
        else:
            expires = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expires})
        encode_jwt = encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

        return encode_jwt, expires

    def decode_token(self):
        try:
            decode_token = decode(
                self.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return decode_token if decode_token["exp"] >= time.time() else None
        except:
            return None

    @staticmethod
    def extract_token(token: str):
        return decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def verify_jwt(jwt_token: str):
    decode_info = decode(
        jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    return decode_info if decode_info is not None else None


async def get_auth_user(
    response: Response,
    access_token: str = Depends(APIKeyCookie(name="access_token", auto_error=True)),
    session: Session = Depends(get_session),
):
    try:
        credentials = verify_jwt(access_token)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "status": "Forbidden",
                    "message": "Invalid token or expired token.",
                },
            )

        if credentials["exp"] < time.time():
            response.delete_cookie(key="access_token")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "status": "Forbidden",
                    "message": "Expired token",
                },
            )

        user = await UserService.get_user_profile(
            session=session, user_id=credentials["id"]
        )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status": "Forbidden",
                "message": "Token is invalid",
            },
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status": "Forbidden",
                "message": "Expired token",
            },
        )


CurrentUser = Depends(get_auth_user)
