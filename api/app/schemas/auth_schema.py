import logging
import re
from fastapi import HTTPException
from typing import TypeVar
from pydantic import BaseModel, field_validator, EmailStr

from ..models.person import Sex

T = TypeVar("T")

logger = logging.getLogger(__name__)


class RegisterSchema(BaseModel):
    email: EmailStr
    name: str
    password: str
    phone_number: str
    birth: str
    sex: Sex
    profile: str = "base64"

    # Sex validation
    @field_validator("sex")
    @classmethod
    def sex_validation(cls, v):
        if hasattr(Sex, v.value) is False:
            raise HTTPException(status_code=400, detail="Invalid input sex")
        return v


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordSchema(BaseModel):
    email: EmailStr
    new_password: str


class DetailSchema(BaseModel):
    status: str
    message: str
    result: T | None = None


class ResponseSchema(BaseModel):
    detail: str
    result: T | None = None
