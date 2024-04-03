from sqlalchemy import Column, Float, Integer, String

from app.core.db import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String, unique=True, index=True)
    balance = Column(Float)
    version = Column(Integer, default=0)
