from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime, date


class TripBase(BaseModel):
    title: str
    destination: str
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("End date must be after start date")
        return self


class TripCreate(TripBase):
    pass

class TripUpdate(TripBase):
    title: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("End date must be on or after start date")
        return self





class TripResponse(TripBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
