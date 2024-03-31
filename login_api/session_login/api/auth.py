from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from model import User
from schema import UserCreate
from services.authentication import authenticate_user, create_session, delete_session
from services.hashing import hash_password

router = APIRouter()


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(user_login: UserLogin, response: Response, db: Session = Depends(get_db)):
    username = user_login.username
    password = user_login.password
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    session = create_session(user.user_id, db)
    response.set_cookie(
        key="session_id", value=session.session_id, httponly=False
    )  # 쿠키 설정
    return {"detail": "Logged in successfully"}


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username, password_hash=hashed_password, email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "user_id": db_user.user_id,
        "username": db_user.username,
        "email": db_user.email,
    }


@router.delete("/logout")
def logout(
    response: Response, session_id: str = Cookie(None), db: Session = Depends(get_db)
):
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Session ID not provided"
        )

    # 데이터베이스에서 세션 삭제
    delete_session(session_id, db)
    # 쿠키 삭제
    response.delete_cookie("session_id")
    return {"detail": "Logged out successfully"}
