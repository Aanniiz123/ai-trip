from sqlalchemy import Column, Integer, String, Date, DateTime, func, ForeignKey
from src.database import Base
from sqlalchemy.orm import relationship


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey('users.id'), nullable= False)
    owner = relationship('User', back_populates='trips')