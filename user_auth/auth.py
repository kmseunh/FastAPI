from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from model import User
from schemas import Token, UserCreate
from setting import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)

router = APIRouter(prefix="/auth", tags=["auth"])


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserCreate):
    create_user_model = User(
        username=create_user_request.username,
        password_hash=pbkdf2_sha256.hash(create_user_request.password),
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )
    access_token = create_token(user.username, user.user_id, timedelta(minutes=1))
    refresh_token = create_token(
        user.username,
        user.user_id,
        timedelta(days=REFRESH_TOKEN_EXPIRE_MINUTES),
        is_refresh=True,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    db: db_dependency, refresh_token: str = Depends(oauth2_bearer)
):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        user = authenticate_user(username, None, db, is_refresh=True)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        access_token = create_token(
            user.username, user.user_id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        ) from exc


def authenticate_user(
    username: str, password: str, db: db_dependency, is_refresh: bool = False
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not is_refresh and not pbkdf2_sha256.verify(password, user.password_hash):
        return False
    return user


def create_token(
    username: str, user_id: int, expires_delta: timedelta, is_refresh: bool = False
) -> str:
    encode = {"sub": username, "id": user_id}
    if is_refresh:
        encode.update({"refresh": True})
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": user_id}
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        ) from exc
