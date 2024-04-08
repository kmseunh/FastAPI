from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.auth.enum import Gender


class UserBase(BaseModel):
    name: str
    username: str
    email: str
    dob: Optional[date] = None
    gender: Optional[Gender] = None
    profile_pic: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    profile_pic: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None


class User(UserBase):
    id: int
    created_dt: datetime

    class Config:
        orm_mod: True
