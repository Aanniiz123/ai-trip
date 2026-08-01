from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from src.database import Base
from sqlalchemy.orm import foreign, relationship



class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"),
        unique=True, nullable=False, index=True
    )

    # Contact & personal
    phone = Column(String(20), nullable=True)
    education = Column(String(255), nullable=True)
    job_title = Column(String(255), nullable=True)
    current_location = Column(String(255), nullable=True)
    nationality = Column(String(100), nullable=True)

    # Preferences (travel-relevant)
    preferred_currency = Column(String(3), nullable=False, default="USD")
    
    user = relationship("User", back_populates="profile")
    
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )


    ## Relationship with Another models
    trips = relationship("Trip", back_populates="owner")
    profile = relationship(
        "UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )