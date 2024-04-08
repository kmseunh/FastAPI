from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from app.auth.models import User
from app.auth.schemas import User as UserSchema
from app.auth.schemas import UserCreate, UserUpdate
from app.core.config import settings
from app.core.db import get_db

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


# username으로 조회
async def get_user_by_username(username: str, db: Session = Depends(get_db)) -> User:
    return db.query(User).filter(User.username == username).first()


async def get_user_by_user_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


# 유저 체크
async def existing_user(
    username: str, email: str, db: Session = Depends(get_db)
) -> bool:
    db_username = db.query(User).filter(User.username == username).first()
    db_email = db.query(User).filter(User.email == email).first()

    if db_username or db_email:
        return True

    return False


# 토큰 생성
async def create_access_token(user: UserSchema) -> str:
    encode = {"sub": user.username, "id": user.id}
    expires = datetime.utcnow() + timedelta(days=settings.EXPIRE_TIME)
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# 현재 user 가져오기
async def get_current_user(
    token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        expires_timestamp = payload.get("exp")
        expires = datetime.utcfromtimestamp(expires_timestamp)
        if expires < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        user = await get_user_by_username(username, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return user
    except (JWTError, HTTPException) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from exc


async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(
            name=user.name or None,
            username=user.username.lower().strip(),
            email=user.email.lower().strip(),
            password_hash=bcrypt_context.hash(user.password),
            dob=user.dob or None,
            gender=user.gender or None,
            bio=user.bio or None,
            location=user.location or None,
            profile_pic=user.profile_pic or None,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        ) from exc


async def authenticate_user(username: str, password: str, db: Session) -> User:
    user = await get_user_by_username(username, db)
    if not user or not bcrypt_context.verify(password, user.password_hash):
        return False
    return user


async def update_user(
    db_user: UserSchema, user_update: UserUpdate, db: Session = Depends(get_db)
):
    for field, value in user_update.dict().items():
        setattr(db_user, field, value or getattr(db_user, field))
    db.commit()
