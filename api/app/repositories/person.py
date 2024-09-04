from sqlmodel import Session, select

from .base import BaseRepo
from ..models.person import Person


class PersonRepo(BaseRepo):
    model = Person

    @staticmethod
    async def find_by_name(session: Session, name: str) -> Person | None:
        query = select(Person).where(Person.name == name)
        return session.exec(query).one_or_none()
