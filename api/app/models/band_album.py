from datetime import date
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship

from ..core.config import GenreChoices


class BandBase(SQLModel):
    name: str
    genre: GenreChoices


class Band(BandBase, table=True):
    __tablename__ = "bands"

    id: int = Field(default=None, primary_key=True)
    albums: list["Album"] = Relationship(
        back_populates="band", cascade_delete=True
    )  # "band" here refer to the attribute field


class BandCreate(BandBase):
    albums: list["AlbumBase"] | None = None

    @field_validator("genre", mode="before")
    def title_case_genre(cls, value):
        return value.title()


class AlbumBase(SQLModel):
    title: str
    release_date: date


class Album(AlbumBase, table=True):
    __tablename__ = "albums"

    id: int = Field(default=None, primary_key=True)
    band_id: int = Field(foreign_key="bands.id")  # "bands.id" is the actual foreign key
    band: Band = Relationship(
        back_populates="albums"
    )  # "albums" here refer to the attribute field
