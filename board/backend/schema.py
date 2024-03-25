from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator


class AnswerCreate(BaseModel):
    content: str

    @field_validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime


class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime
    answers: List[Answer] = []  # 리스트 형식을 직접 가져옵니다.

    class Config:
        from_attributes = True
