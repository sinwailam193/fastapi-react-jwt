import logging
import re
from fastapi import HTTPException
from typing import TypeVar
from pydantic import BaseModel, field_validator

from ..models.person import Sex

T = TypeVar("T")

logger = logging.getLogger(__name__)


class RegisterSchema(BaseModel):
    email: str
    name: str
    password: str
    phone_number: str
    birth: str
    sex: Sex
    profile: str = "base64"

    # phone number validation
    @field_validator("phone_number")
    def phone_validaton(self, v):
        logger.debug(f"phone in 2 validator: {v}")

        # regex phone number
        regex = r"^[\+]?[(]?[0-9]{4}[)]?[-\s\.]?[0-9]{4}[-\s\.]?[0-9]{4,6}$"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail="Invalid input phone number!")
        return v

    # Sex validation
    @field_validator("sex")
    def sex_validation(cls, v):
        if hasattr(Sex, v) is False:
            raise HTTPException(status_code=400, detail="Invalid input sex")
        return v


class LoginSchema(BaseModel):
    email: str
    password: str


class ForgotPasswordSchema(BaseModel):
    email: str
    new_password: str


class DetailSchema(BaseModel):
    status: str
    message: str
    result: T | None = None


class ResponseSchema(BaseModel):
    detail: str
    result: T | None = None
