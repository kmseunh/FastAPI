from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette import status

import schema
from api.answer.answer_crud import create_answer
from api.question import question_crud
from database import get_db

router = APIRouter(prefix="/api/answer")


@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(
    question_id: int,
    _answer_create: schema.AnswerCreate,
    db: Session = Depends(get_db),
):

    # create answer
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    create_answer(db, question=question, answer_create=_answer_create)


# @router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
# def answer_create(
#     question_id: int,
#     _answer_create: schema.AnswerCreate,
#     db: Session = Depends(get_db),
# ):

#     # create answer
#     question = db.execute(
#         text("SELECT * FROM question WHERE id = ?"), (question_id,)
#     ).fetchone()

#     if not question:
#         raise HTTPException(status_code=404, detail="Question not found")

#     db.execute(
#         text("INSERT INTO answer (text, question_id) VALUES (?, ?)"),
#         (_answer_create.text, question_id),
#     )
#     db.commit()
