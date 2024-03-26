from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator


def validate_not_empty(value):
    if not value or not value.strip():
        raise ValueError("빈 값은 허용되지 않습니다.")
    return value


class AnswerCreate(BaseModel):
    content: str

    _validate_content = field_validator("content")(validate_not_empty)


class QuestionCreate(BaseModel):
    subject: str
    content: str

    _validate_subject_content = field_validator("subject", "content")(
        validate_not_empty
    )


class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime


class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime
    answers: List[Answer] = []

    class Config:
        from_attributes = True


class QuestionList(BaseModel):
    total: int = 0
    question_list: List[Question] = []
