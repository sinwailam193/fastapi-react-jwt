from typing import List
from sqlmodel import Session, select

from .base import BaseRepo
from ..models.person import Role


class RoleRepo(BaseRepo):
    model = Role

    @staticmethod
    async def find_by_role_name(session: Session, role_name: str) -> Role | None:
        query = select(Role).where(Role.role_name == role_name)
        return session.exec(query).one_or_none()

    @staticmethod
    async def find_by_list_role_name(
        session: Session, role_names: List[str]
    ) -> List[Role]:
        query = select(Role).where(Role.role_name.in_(role_names))
        return session.exec(query).all()

    @staticmethod
    async def create_list(session: Session, roles: List[Role]) -> None:
        session.add_all(roles)
        session.commit()
