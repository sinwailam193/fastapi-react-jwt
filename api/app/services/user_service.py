from sqlmodel import Session, select

from ..models.person import User, Person


class UserService:
    @staticmethod
    async def get_user_profile(session: Session, user_id: int):
        query = (
            select(
                User.email,
                Person.name,
                Person.birth,
                Person.sex,
                Person.phone_number,
            )
            .join(Person)
            .where(User.id == user_id)
        )
        return session.exec(query).mappings().one()
