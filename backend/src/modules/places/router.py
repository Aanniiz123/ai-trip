
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.modules.users.users_profile import User
from src.modules.auth.service import get_current_active_user
from src.modules.places.models import Place
from src.modules.places.schemas import CityRequest, PlaceCreate, PlaceResponse
from src.modules.places.service import places_service, create_place

router = APIRouter(prefix="/places", tags=["places"])


@router.post("/search")
async def search_place(body: CityRequest):
    return await places_service.search_city(body.city)


@router.post("/", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
async def save_place(
    place_data: PlaceCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_place(db, current_user.id, place_data)


@router.get("/", response_model=List[PlaceResponse])
async def list_places(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return db.query(Place).filter(Place.user_id == current_user.id).all()


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_place(
    place_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    place = db.query(Place).filter(Place.id == place_id, Place.user_id == current_user.id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    db.delete(place)
    db.commit()
