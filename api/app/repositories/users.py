from sqlmodel import Session, select, update as sql_update

from ..models.person import User
from .base import BaseRepo


class UserRepo(BaseRepo):
    model = User

    @staticmethod
    async def find_by_email(session: Session, email: str) -> User | None:
        query = select(User).where(User.email == email)
        return session.exec(query).one_or_none()

    @staticmethod
    async def update_password(session: Session, email: str, new_password: str) -> None:
        query = (
            sql_update(User)
            .where(User.email == email)
            .values(password=new_password)
            .execution_options(synchronize_session="fetch")
        )
        session.exec(query)
        session.commit()
