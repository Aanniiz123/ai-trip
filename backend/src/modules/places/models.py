
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, func
from src.database import Base

class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    latitude = Column(DECIMAL(10, 7), nullable=True)
    longitude = Column(DECIMAL(10, 7), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
