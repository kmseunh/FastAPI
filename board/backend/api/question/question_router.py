from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from starlette import status

import schema
from api.question import question_crud

# from database import SessionLocal
from database import get_db

router = APIRouter(prefix="/api/question")


@router.get("/list", response_model=schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    print(page)
    print(size)
    total, _question_list = question_crud.get_question_list(
        db, skip=page * size, limit=size
    )
    return {"total": total, "question_list": _question_list}


@router.get("/detail/{question_id}", response_model=schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(
    _question_create: schema.QuestionCreate, db: Session = Depends(get_db)
):
    question_crud.create_question(db=db, question_create=_question_create)


# @router.get("/detail/{question_id}", response_model=schemas.Question)
# def question_detail(question_id: int, db: Session = Depends(get_db)):
#     # 직접 SQL 쿼리를 실행합니다.
#     query = f"SELECT * FROM question WHERE id = :question_id"
#     result = db.execute(query, {"question_id": question_id})
#     return result
