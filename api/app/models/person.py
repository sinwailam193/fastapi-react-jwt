from datetime import date
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column, String

from .mixins import TimeMixin


class Sex(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class UsersRole(SQLModel, TimeMixin, table=True):
    __tablename__ = "users_roles"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role_id: int = Field(foreign_key="roles.id", primary_key=True)


class Role(SQLModel, TimeMixin, table=True):
    __tablename__ = "roles"

    id: int = Field(None, primary_key=True, nullable=False)
    role_name: str

    users: list["User"] = Relationship(back_populates="roles", link_model=UsersRole)


class Person(SQLModel, TimeMixin, table=True):
    __tablename__ = "people"

    id: int = Field(None, primary_key=True, nullable=False)
    name: str
    birth: date
    sex: Sex | None = None
    profile: str
    phone_number: str

    users: list["User"] = Relationship(back_populates="person", cascade_delete=True)


class User(SQLModel, TimeMixin, table=True):
    __tablename__ = "users"

    id: int = Field(None, primary_key=True, nullable=False)
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str

    person_id: int | None = Field(foreign_key="people.id")
    person: Person | None = Relationship(back_populates="users")

    roles: list[Role] = Relationship(back_populates="users", link_model=UsersRole)
