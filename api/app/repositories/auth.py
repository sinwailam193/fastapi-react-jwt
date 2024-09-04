import time
from typing import Dict, Any
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
    def __init__(self, auto_error: bool = True) -> None:
        super(JWTBearer, self).__init__(auto_error=auto_error)
