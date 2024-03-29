from fastapi import APIRouter, Depends

from model import User
from services.authentication import get_user_by_session

router = APIRouter()


@router.get("/protected_resource")
def get_protected_resource(user: User = Depends(get_user_by_session)):
    return {
        "message": "This is a protected resource",
        "user_id": user.user_id,
        "username": user.username,
    }
