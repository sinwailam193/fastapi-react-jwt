from datetime import date
from pydantic import field_validator, validator
from sqlmodel import SQLModel, Field, Relationship

from app.core.config import GenreChoices


class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int = Field(foreign_key="band.id")


class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="albums")


class BandBase(SQLModel):
    name: str
    genre: GenreChoices


class BandCreate(BandBase):
    albums: list[AlbumBase] | None = None

    @field_validator("genre", mode="before")
    def title_case_genre(cls, value):
        return value.title()


class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")
