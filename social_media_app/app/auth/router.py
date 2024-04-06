from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.schemas import UserCreate, UserUpdate
from app.auth.service import (
    authenticate_user,
    create_access_token,
    create_user,
    existing_user,
    get_current_user,
)
from app.auth.service import update_user as update_user_svc
from app.core.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = await existing_user(user.username, user.email, db)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email is already in use",
        )

    created_user = await create_user(user, db)

    return {
        "user": created_user,
    }


@router.post("/token", status_code=status.HTTP_201_CREATED)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = await authenticate_user(form_data.username, form_data.password, db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
        )

    access_token = await create_access_token(db_user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile", status_code=status.HTTP_200_OK, response_model=UserUpdate)
async def current_user(token: str, db: Session = Depends(get_db)):
    db_user = await get_current_user(token, db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
        )
    return db_user


@router.put("/update/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    username: str, token: str, user_update: UserUpdate, db: Session = Depends(get_db)
):
    db_user = await get_current_user(token, db)
    if db_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not authorized to update this user",
        )
    await update_user_svc(db_user, user_update, db)
