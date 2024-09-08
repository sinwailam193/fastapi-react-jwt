import time
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials
from datetime import timedelta, datetime, timezone
from jose.jwt import encode, decode

from ..core.config import settings


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

        return encode_jwt

    def decode_token(self):
        try:
            decode_token = decode(
                self.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return decode_token if decode_token["exp"] >= time.time() else None
        except:
            return {}

    @staticmethod
    def extract_token(token: str):
        return decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


class JWTBearer(HTTPException):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "status": "Forbidden",
                        "message": "Invalid authentication schema.",
                    },
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "status": "Forbidden",
                        "message": "Invalid token or expired token.",
                    },
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "status": "Forbidden",
                    "message": "Invalid authorization code.",
                },
            )

    @staticmethod
    def verify_jwt(jwt_token: str):
        return (
            True
            if decode(jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            is not None
            else False
        )
