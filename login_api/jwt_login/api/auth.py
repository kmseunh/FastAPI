from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from model import User
from schemas import UserCreate, UserLogin
from service.authentication import (
    authenticate_user,
    create_access_token,
    get_user_by_token,
)
from service.hashing import hash_password
from setting import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.get("/protected_resource")
async def get_protected_resource(user: str = Depends(get_user_by_token)):
    return {"message": "This is a protected resource", "user": user}


@router.post("/login")
def login(user_login: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(user_login, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        # secure=True,  # HTTPS 연결을 통해서만 쿠키 전송
        # samesite="Strict",  # SameSite 설정
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserCreate)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 사용자가 이미 존재하는지 확인합니다.
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
