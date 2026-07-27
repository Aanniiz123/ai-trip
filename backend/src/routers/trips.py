from fastapi import APIRouter, Depends, HTTPException
from src.schemas.trip import TripResponse, TripCreate, TripUpdate
from src.model.trip import Trip
from src.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/trips", tags=["trips"])

@router.get("/", response_model=list[TripResponse])
def get_trips(db: Session = Depends(get_db)):
    trips = db.query(Trip).all()
    return trips

@router.post("/", response_model=TripResponse)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    db_trip = Trip(**trip.model_dump())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: int, trip: TripUpdate, db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    for field, value in trip.model_dump(exclude_unset=True).items():
        setattr(db_trip, field, value)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.delete("/{trip_id}", response_model=TripResponse)
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(db_trip)
    db.commit()
    return db_trip


