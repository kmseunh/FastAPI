from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True


class SessionCreate(BaseModel):
    user_id: int
    password: str


class Sessions(BaseModel):
    session_id: str
    user_id: int
    create_time: datetime
    expire_time: datetime

    class Config:
        orm_mode = True
