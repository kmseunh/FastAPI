from typing import Optional

from pydantic import BaseModel

from app.auth.schemas import UserBase


class Profile(UserBase):
    followers_count: Optional[int] = 0
    followings_count: Optional[int] = 0

    class Config:
        orm_mode = True
        from_attributes = True


class UserSchema(BaseModel):
    profile_pic: Optional[str] = None
    username: str
    name: Optional[str] = None

    class Config:
        orm_mode = True


class FollowerList(BaseModel):
    followers: list[UserSchema] = []


class FollowingList(BaseModel):
    followings: list[UserSchema] = []
