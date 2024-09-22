from sqlmodel import Session, select, delete as sql_delete

from ..models.person import RefreshToken
from .base import BaseRepo


class RefreshTokenRepo(BaseRepo):
    model = RefreshToken

    @staticmethod
    async def find_by_token(session: Session, token: str) -> RefreshToken | None:
        query = select(RefreshToken).where(RefreshToken.token == token)
        return session.exec(query).one_or_none()

    @staticmethod
    async def find_by_user_id(session: Session, user_id: int) -> RefreshToken | None:
        query = select(RefreshToken).where(RefreshToken.user_id == user_id)
        return session.exec(query).one_or_none()
