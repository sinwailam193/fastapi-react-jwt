from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..core.db import get_session
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
