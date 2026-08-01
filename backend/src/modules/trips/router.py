
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.modules.users.users_profile import User
from src.modules.auth.service import get_current_active_user
from src.modules.trips.schemas import TripCreate, TripUpdate, TripResponse
from src.modules.trips.service import get_trips, create_trip, get_trip, update_trip, delete_trip

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("/", response_model=List[TripResponse])
async def list_trips(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return get_trips(db, current_user.id)


@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_new_trip(
    trip_data: TripCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_trip(db, trip_data, current_user.id)


@router.get("/{trip_id}", response_model=TripResponse)
async def get_single_trip(
    trip_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    trip = get_trip(db, trip_id, current_user.id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.put("/{trip_id}", response_model=TripResponse)
async def update_existing_trip(
    trip_id: int,
    trip_data: TripUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    trip = update_trip(db, trip_id, trip_data, current_user.id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_trip(
    trip_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    trip = delete_trip(db, trip_id, current_user.id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
