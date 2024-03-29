import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=False)

    sessions = relationship("Sessions", back_populates="user")


class Sessions(Base):
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    create_time = Column(DateTime, default=func.now())
    expire_time = Column(DateTime)

    user = relationship("User", back_populates="sessions")
