from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.sql import text

import schema
from models import Question


def get_question_list(db: Session, skip: int = 0, limit: int = 10):
    _question_list = db.query(Question).order_by(Question.create_date.desc())

    total = _question_list.count()
    question_list = _question_list.offset(skip).limit(limit).all()
    return total, question_list


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


# def get_question_list(db: Session, skip: int = 0, limit: int = 10):
#     sql_query = """
#     SELECT *
#     FROM question
#     ORDER BY create_date DESC
#     OFFSET :skip LIMIT :limit;
#     """

#     total_query = "SELECT COUNT(*) FROM question;"

#     question_list = db.execute(sql_query, {"skip": skip, "limit": limit}).fetchall()
#     total = db.execute(total_query).scalar()

#     return total, question_list


# def get_question(db: Session, question_id: int):
#     query = f"SELECT * FROM question WHERE id = {question_id}"
#     question = db.execute(query)
#     return question
