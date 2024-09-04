from datetime import datetime
from pydantic import BaseModel
from sqlmodel import Field, Column, DateTime


class TimeMixin(BaseModel):
    """Mixin for datetime value of when the entity was created and when it was last updated"""

    created_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime,
            default=datetime.now,
            onupdate=datetime.now,
            nullable=False,
        )
    )
