from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.service import existing_user, get_current_user, get_user_by_username
from app.core.db import get_db
from app.profile.schemas import FollowerList, FollowingList, Profile
from app.profile.service import (
    follow_svc,
    get_followers_svc,
    get_followings_svc,
    unfollow_svc,
)

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/user/{username}", response_model=Profile)
async def profile(username: str, db: Session = Depends(get_db)):
    db_user_exist = await existing_user(username, "", db)
    if not db_user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invaild username"
        )

    db_user = await get_user_by_username(username, db)

    user_profile = Profile.from_orm(db_user)
    return user_profile


@router.post("/follow/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def follow(username: str, token: str, db: Session = Depends(get_db)):
    db_user = await get_current_user(token, db)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid token"
        )

    res = await follow_svc(db, db_user.username, username)
    if res == False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="could not follow"
        )


@router.post("/unfollow/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow(username: str, token: str, db: Session = Depends(get_db)):
    db_user = await get_current_user(token, db)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid token"
        )

    res = await unfollow_svc(db, db_user.username, username)
    if res == False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="could not follow"
        )


@router.get("/followers", response_model=FollowerList)
async def get_followers(token: str, db: Session = Depends(get_db)):
    current_user = await get_current_user(token, db)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    return await get_followers_svc(db, current_user.id)


@router.get("/followings", response_model=FollowingList)
async def get_followings(token: str, db: Session = Depends(get_db)):
    current_user = await get_current_user(token, db)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
        )
    print(current_user.id)
    return await get_followings_svc(db, current_user.id)
