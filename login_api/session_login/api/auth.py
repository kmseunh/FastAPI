from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from model import User
from schema import UserCreate
from services.authentication import authenticate_user, create_session
from services.hashing import hash_password

router = APIRouter()


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    username = user_login.username
    password = user_login.password
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    session = create_session(user.user_id, db)
    return {"session_id": session.session_id}


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
