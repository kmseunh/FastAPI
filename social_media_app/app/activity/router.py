from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.activity.service import get_activites_by_username
from app.core.db import get_db

router = APIRouter(prefix="/activity", tags=["activity"])


@router.get("/user/{username}")
async def activity(
    username: str, page: int = 1, limit: int = 10, db: Session = Depends(get_db)
):
    return await get_activites_by_username(db, username, page, limit)
