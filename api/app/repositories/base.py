from typing import TypeVar, Generic
from sqlmodel import Session, update as sql_update, delete as sql_delete, select

T = TypeVar("T")


class BaseRepo:
    model = Generic[T]

    @classmethod
    async def create(self, session: Session, **kwargs):
        new_model = self.model(**kwargs)

        session.add(new_model)
        session.commit()
        session.refresh(new_model)
        return new_model

    @classmethod
    async def get_all(self, session: Session):
        query = select(self.model)
        return session.exec(query).all()

    @classmethod
    async def get_by_id(self, session: Session, id: int):
        return session.get(self.model, id)

    @classmethod
    async def update(self, session: Session, id: int, **kwargs):
        query = (
            sql_update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        session.exec(query)
        session.commit()

    @classmethod
    async def delete(self, session: Session, id: int):
        query = sql_delete(self.model).where(self.model.id == id)
        session.exec(query)
        session.commit()
