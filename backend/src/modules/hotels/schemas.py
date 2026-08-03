from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class HotelsSearchRequest(BaseModel):
    place: str  


class HotelsResult(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    categories: Optional[list] = None
    website: Optional[str] = None
    phone: Union[str, int, None] = None
  
    
class HotelHistoryRead(BaseModel):
    id: int
    place: str
    hotel_name: Optional[str] = None
    searched_at: datetime
    class Config:
        from_attributes = True
        