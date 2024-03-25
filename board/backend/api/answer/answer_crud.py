from datetime import datetime

from sqlalchemy.orm import Session

import schema
from models import Answer, Question


def create_answer(db: Session, question: Question, answer_create: schema.AnswerCreate):
    db_answer = Answer(
        question=question, content=answer_create.content, create_date=datetime.now()
    )
    db.add(db_answer)
    db.commit()


# def create_answer(db: Session, question: Question, answer_create: schema.AnswerCreate):
#     create_date = datetime.now()
#     query = """
#         INSERT INTO answer (question_id, content, create_date)
#         VALUES (?, ?, ?)
#     """
#     values = {
#         "question_id": question.id,
#         "content": answer_create.content,
#         "create_date": create_date,
#     }
#     db.execute(query, values)
#     db.commit()
