from fastapi import APIRouter, Depends, HTTPException
from src.modules.hotels.schemas import HotelsSearchRequest, HotelsResult, HotelHistoryRead
from src.modules.hotels.service import hotels_service
from typing import List
from sqlalchemy.orm import Session


from src.database import get_db
from src.modules.auth.service import get_current_active_user
from src.modules.hotels.models import HotelSearchHistory


router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.post("/search", response_model=List[HotelsResult])
async def search_hotels(
    body: HotelsSearchRequest,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return await hotels_service.search_hotels(
        place=body.place,
        user_id=current_user.id,
        db=db,
    )
    

@router.get("/history", response_model=List[HotelHistoryRead])
def get_search_history(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return (
        db.query(HotelSearchHistory)
        .filter(HotelSearchHistory.user_id == current_user.id)
        .order_by(HotelSearchHistory.searched_at.desc())
        .all()
    )
