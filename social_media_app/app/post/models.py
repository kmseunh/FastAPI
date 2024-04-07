from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.core.db import Base

post_hashtags = Table(
    "post_hashtags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("hashtag_id", Integer, ForeignKey("hashtags.id")),
)

post_likes = Table(
    "post_likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("post_id", Integer, ForeignKey("posts.id")),
)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    image = Column(String)
    location = Column(String)
    created_dt = Column(DateTime, default=datetime.now)
    likes_count = Column(Integer, default=0)

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

    hashtags = relationship("Hashtag", secondary=post_hashtags, back_populates="posts")
    like_by_users = relationship(
        "User", secondary=post_likes, back_populates="liked_posts"
    )


class Hashtag(Base):
    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    posts = relationship("Post", secondary=post_hashtags, back_populates="hashtags")
