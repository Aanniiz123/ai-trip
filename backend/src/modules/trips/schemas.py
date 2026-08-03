
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, model_validator, ConfigDict
from src.modules.trips.models import TripType


class TripBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    destination: str = Field(..., min_length=1, max_length=255)
    start_date: date
    end_date: date
    trip_type: TripType = TripType.SOLO
    num_people: int = Field(1, ge=1, le=50)
    num_days: Optional[int] = Field(None, ge=1, le=365)
    budget: Optional[Decimal] = Field(None, ge=0)
    currency: str = Field("USD", min_length=3, max_length=3)
    audience: str = Field("foreign", pattern="^(local|foreign)$")
    is_completed: bool = False

    @model_validator(mode="after")
    def _check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        self.num_days = (self.end_date - self.start_date).days
        return self


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    # all optional for PATCH
    title: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    trip_type: Optional[TripType] = None
    num_people: Optional[int] = Field(None, ge=1, le=50)
    num_days: Optional[int] = Field(None, ge=1, le=365)
    budget: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = None
    audience: Optional[str] = None
    is_completed: Optional[bool] = None


class TripRead(TripBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

TripResponse = TripRead
