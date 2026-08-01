from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ProfileBase(BaseModel):
    phone: Optional[str] = Field(None, max_length=20)
    education: Optional[str] = Field(None, max_length=255)
    job_title: Optional[str] = Field(None, max_length=255)
    current_location: Optional[str] = Field(None, max_length=255)
    nationality: Optional[str] = Field(None, max_length=100)
    preferred_currency: str = Field("USD", min_length=3, max_length=3)
    date_of_birth: Optional[date] = None
    avatar_url: Optional[str] = Field(None, max_length=500)


class ProfileRead(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class ProfileUpdate(BaseModel):
    phone: Optional[str] = None
    education: Optional[str] = None
    job_title: Optional[str] = None
    current_location: Optional[str] = None
    nationality: Optional[str] = None
    preferred_currency: Optional[str] = None
    date_of_birth: Optional[date] = None
    avatar_url: Optional[str] = None
    


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


## for the jwt Token

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None