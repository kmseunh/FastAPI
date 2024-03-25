from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

import schema
from api.question import question_crud

# from database import SessionLocal
from database import get_db

router = APIRouter(prefix="/api/question")


@router.get("/list", response_model=list[schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.get_question_list(db)
    return _question_list


@router.get("/detail/{question_id}", response_model=schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question


# @router.get("/list", response_model=list[schema.Question])
# def question_list(db: Session = Depends(get_db)):
#     _question_list = qustion_crud.get_question_list(db)
#     return _question_list


# @router.get("/detail/{question_id}", response_model=schemas.Question)
# def question_detail(question_id: int, db: Session = Depends(get_db)):
#     # 직접 SQL 쿼리를 실행합니다.
#     query = f"SELECT * FROM question WHERE id = :question_id"
#     result = db.execute(query, {"question_id": question_id})
#     return result
