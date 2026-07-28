from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from src.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    trip = relationship("Trip", back_populates="activities")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
