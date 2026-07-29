                                                                                                                    
from typing import Annotated                                                                                        
from fastapi import APIRouter, Depends, HTTPException                                                               
from sqlalchemy.orm import Session                                                                                  
from src.schemas.trip import TripResponse, TripCreate, TripUpdate                                                   
from src.model.trip import Trip                                                                                     
from src.model.user import User                                                                                     
from src.database import get_db                                                                                     
from src.routers.auth import get_current_active_user

router = APIRouter(prefix="/trips", tags=["trips"])                                                                 
@router.get("/", response_model=list[TripResponse])

def get_trips(                                                                                                      
    current_user: Annotated[User, Depends(get_current_active_user)],                                                
    db: Session = Depends(get_db),                                                                                  
):                                                                                                                  
    # Only return trips belonging to the logged-in user                                                             
    return db.query(Trip).filter(Trip.user_id == current_user.id).all()


@router.post("/", response_model=TripResponse)                                                                      
def create_trip(                                                                                                    
    trip: TripCreate,                                                                                               
    current_user: Annotated[User, Depends(get_current_active_user)],                                                
    db: Session = Depends(get_db),                                                                                  
):                                                                                                                  
    db_trip = Trip(**trip.model_dump(), user_id=current_user.id)  # attach owner                                    
    db.add(db_trip)                                                                                                 
    db.commit()                                                                                                     
    db.refresh(db_trip)                                                                                             
    return db_trip


@router.get("/{trip_id}", response_model=TripResponse)                                                              
def get_trip(                                                                                                       
    trip_id: int,                                                                                                   
    current_user: Annotated[User, Depends(get_current_active_user)],                                                
    db: Session = Depends(get_db),                                                                                  
):                                                                                                                  
    db_trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()                    
    if not db_trip:                                                                                                 
        raise HTTPException(status_code=404, detail="Trip not found")                                               
    return db_trip


@router.put("/{trip_id}", response_model=TripResponse)                                                              
def update_trip(                                                                                                    
    trip_id: int,                                                                                                   
    trip: TripUpdate,                                                                                               
    current_user: Annotated[User, Depends(get_current_active_user)],                                                
    db: Session = Depends(get_db),                                                                                  
):                                                                                                                  
    db_trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()                    
    if not db_trip:                                                                                                 
        raise HTTPException(status_code=404, detail="Trip not found")                                               
    for field, value in trip.model_dump(exclude_unset=True).items():                                                
        setattr(db_trip, field, value)                                                                              
    db.commit()                                                                                                     
    db.refresh(db_trip)                                                                                             
    return db_trip                                                                                                  


@router.delete("/{trip_id}", response_model=TripResponse)
def delete_trip(                                                                                                    
    trip_id: int,                                                                                                   
    current_user: Annotated[User, Depends(get_current_active_user)],                                                
    db: Session = Depends(get_db),                                                                                  
):                                                                                                                  
    db_trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()                    
    if not db_trip:                                                                                                 
        raise HTTPException(status_code=404, detail="Trip not found")                                               
    db.delete(db_trip)                                                                                              
    db.commit()                                                                                                     
    return db_trip  