from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlmodel import Session, select

from ..core.db import get_session
from ..core.config import GenreChoices
from ..models.band_album import Band, BandCreate, Album

router = APIRouter()


@router.post("")
async def create_band(
    band_data: BandCreate, session: Session = Depends(get_session)
) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(
                title=album.title, release_date=album.release_date, band=band
            )
            session.add(album_obj)

    session.commit()
    session.refresh(band)
    return band


@router.get("")
async def get_band(
    genre: GenreChoices | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None,
    session: Session = Depends(get_session),
) -> list[Band]:
    if genre is not None:
        band_list = session.exec(select(Band).where(Band.genre == genre))
    else:
        band_list = session.exec(select(Band)).all()

    return band_list


@router.get("/{band_id}")
async def get_band(
    band_id: Annotated[int, Path(title="The band ID")],
    session: Session = Depends(get_session),
) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Band is not found"
        )
    return band
