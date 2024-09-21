from fastapi import status, HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlmodel import Session

from ..core.config import settings
from ..schemas.auth_schema import RegisterSchema, LoginSchema, ForgotPasswordSchema
from ..models.person import Person, User, UsersRole
from ..repositories.role import RoleRepo
from ..repositories.person import PersonRepo
from ..repositories.users import UserRepo
from ..repositories.users_role import UsersRoleRepo
from ..repositories.auth import JWTRepo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    async def register_service(session: Session, register: RegisterSchema):
        # checking if email is created already exists
        exist_user = await UserRepo.find_by_email(session=session, email=register.email)
        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

        # convert birth str to date
        birth_date = datetime.strptime(register.birth, "%d-%m-%Y")

        # mapping request data to class entity table
        _person = Person(
            name=register.name,
            birth=birth_date,
            sex=register.sex,
            profile="",
            phone_number=register.phone_number,
        )
        _person = await PersonRepo.create(session=session, **_person.model_dump())

        _user = User(
            email=register.email,
            password=pwd_context.hash(register.password),
            person_id=_person.id,
        )
        _user = await UserRepo.create(session=session, **_user.model_dump())

        _role = await RoleRepo.find_by_role_name(session=session, role_name="user")
        _users_role = UsersRole(user_id=_user.id, role_id=_role.id)

        await UsersRoleRepo.create(session=session, **_users_role.model_dump())

        return JWTRepo(data={"id": _user.id}).generate_token(
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    @staticmethod
    async def login_service(session: Session, login: LoginSchema):
        _user = await UserRepo.find_by_email(session=session, email=login.email)

        if not _user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
            )

        if not pwd_context.verify(login.password, _user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password is invalid"
            )

        return JWTRepo(data={"id": _user.id}).generate_token(
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    @staticmethod
    async def fogot_password_service(
        session: Session, forgotPassword: ForgotPasswordSchema
    ):
        _user = await UserRepo.find_by_email(
            session=session, email=forgotPassword.email
        )

        if not _user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Email is not found"
            )

        await UserRepo.update_password(
            session=session,
            email=forgotPassword.email,
            new_password=pwd_context.hash(forgotPassword.new_password),
        )
