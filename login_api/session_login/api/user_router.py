from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from model import User
from schema import UserOut

router = APIRouter()


@router.get(
    "/users",
    response_model=List[UserOut],
)
def get_user_list(db: Session = Depends(get_db)):
    user_list = db.query(User).order_by(User.user_id.asc()).all()
    return user_list
