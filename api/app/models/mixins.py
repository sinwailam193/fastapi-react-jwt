from datetime import datetime
from pydantic import BaseModel
from sqlmodel import Field, func, TIMESTAMP, text


class TimeMixin(BaseModel):
    """Mixin for datetime value of when the entity was created and when it was last updated"""

    created_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    updated_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
        nullable=False,
    )
