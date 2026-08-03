from pydantic import BaseModel
from typing import Optional, Union
class HotelsSearchRequest(BaseModel):
    place: str  # e.g. "Paris" or "New York"
class HotelsResult(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    categories: Optional[list] = None
    website: Optional[str] = None
    phone: Union[str, int, None] = None