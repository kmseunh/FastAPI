from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Hashtag(BaseModel):
    id: int
    name: str


class PostCreate(BaseModel):
    content: Optional[str] = None
    image: str
    location: Optional[str] = None


class Post(PostCreate):
    id: int
    author_id: int
    likes_count: int
    created_dt: datetime
    hashtags: List[Hashtag] = []

    class Config:
        orm_mode = True
