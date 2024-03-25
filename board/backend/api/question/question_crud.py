from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.sql import text

import schema
from models import Question


def get_question_list(db: Session):
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list


def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question


def create_question(db: Session, question_create: schema.QuestionCreate):
    db_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now(),
    )
    db.add(db_question)
    db.commit()


# def get_question_list(db: Session):
#     query = text("SELECT * FROM question ORDER BY create_date DESC;")
#     result = db.execute(query)
#     return [dict(zip(result.keys(), row)) for row in result]


# def get_question(db: Session, question_id: int):
#     query = f"SELECT * FROM question WHERE id = {question_id}"
#     question = db.execute(query)
#     return question
