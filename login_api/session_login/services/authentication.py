from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from model import Sessions, User

from .hashing import verify_password


def create_session(user_id: int, db: Session = Depends(get_db)) -> Session:
    expire_time = datetime.now() + timedelta(days=1)
    new_session = Sessions(user_id=user_id, expire_time=expire_time)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def delete_session(session_id: str, db: Session = Depends(get_db)):
    db.query(Sessions).filter(Sessions.session_id == session_id).delete()
    db.commit()


def get_user_by_session(session_id: str, db: Session = Depends(get_db)) -> User:
    session = db.query(Sessions).filter(Sessions.session_id == session_id).first()
    if not session or session.expire_time < datetime.now():
        if session:
            delete_session(session)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return session.user
