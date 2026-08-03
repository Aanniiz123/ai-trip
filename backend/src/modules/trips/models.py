
import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Enum, ForeignKey, func, DECIMAL, Boolean
)
from sqlalchemy.orm import relationship
from src.database import Base


class TripType(str, enum.Enum):
    SOLO = "solo"
    COUPLE = "couple"
    FAMILY = "family"
    GROUP = "group"


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # NEW fields
    trip_type = Column(
        Enum(TripType, name="trip_type_enum"),
        nullable=False, default=TripType.SOLO
    )
    num_people = Column(Integer, nullable=False, default=1)
    num_days = Column(Integer, nullable=False)            # computed/stored, validated
    budget = Column(DECIMAL(12, 2), nullable=True)
    currency = Column(String(3), nullable=False, default="USD")
    audience = Column(
        Enum("local", "foreign", name="trip_audience_enum"),
        nullable=False, default="foreign"
    )

    is_completed = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="trips")