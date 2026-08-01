
from sqlalchemy.orm import Session

from src.modules.trips.models import Trip
from src.modules.trips.schemas import TripCreate, TripUpdate


def get_trips(db: Session, user_id: int) -> list[Trip]:
    return db.query(Trip).filter(Trip.user_id == user_id).all()


def create_trip(db: Session, trip_data: TripCreate, user_id: int) -> Trip:
    trip = Trip(**trip_data.model_dump(), user_id=user_id)
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


def get_trip(db: Session, trip_id: int, user_id: int) -> Trip | None:
    return db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()


def update_trip(db: Session, trip_id: int, trip_data: TripUpdate, user_id: int) -> Trip | None:
    trip = get_trip(db, trip_id, user_id)
    if not trip:
        return None
    for field, value in trip_data.model_dump(exclude_unset=True).items():
        setattr(trip, field, value)
    db.commit()
    db.refresh(trip)
    return trip


def delete_trip(db: Session, trip_id: int, user_id: int) -> Trip | None:
    trip = get_trip(db, trip_id, user_id)
    if not trip:
        return None
    db.delete(trip)
    db.commit()
    return trip
