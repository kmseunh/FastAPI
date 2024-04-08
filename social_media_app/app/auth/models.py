from datetime import datetime

from sqlalchemy import DATE, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.auth.enum import Gender
from app.core.db import Base
from app.post.models import post_likes


class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    following_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="followers"
    )

    following = relationship(
        "User", foreign_keys=[following_id], back_populates="followings"
    )


class User(Base):
    __tablename__ = "users"

    # 기본 정보
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_dt = Column(DateTime, default=datetime.utcnow)

    # 프로필
    dob = Column(DATE)
    gender = Column(Enum(Gender))
    profile_pic = Column(String)
    bio = Column(String)
    location = Column(String)

    posts = relationship("Post", back_populates="author")
    liked_posts = relationship(
        "Post", secondary=post_likes, back_populates="like_by_users"
    )

    followers = relationship(
        Follow, foreign_keys=[Follow.following_id], back_populates="following"
    )
    followings = relationship(
        Follow, foreign_keys=[Follow.follower_id], back_populates="follower"
    )

    followers_count = Column(Integer, default=0)
    followings_count = Column(Integer, default=0)
