from datetime import datetime

from sqlalchemy import DATE, Column, DateTime, Enum, Integer, String

from app.auth.enum import Gender
from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    # 기본 정보
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_dt = Column(DateTime, default=datetime.utcnow())

    # 프로필
    dob = Column(DATE)
    gender = Column(Enum(Gender))
    profile_pic = Column(String)
    bio = Column(String)
    location = Column(String)
