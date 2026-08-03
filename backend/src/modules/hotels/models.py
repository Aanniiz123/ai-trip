
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database import Base




class HotelSearchHistory(Base):
    __tablename__ = "hotel_search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    place = Column(String(255), nullable=False)
    searched_at = Column(DateTime(timezone=True), server_default=func.now())
