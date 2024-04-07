from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.service import existing_user, get_current_user
from app.core.db import get_db
from app.post.schemas import Post, PostCreate
from app.post.service import (
    create_hashtags_svc,
    create_post_svc,
    delete_post_svc,
    get_post_from_post_id_svc,
    get_posts_from_hashtag_svc,
    get_random_posts_svc,
    get_users_posts_svc,
    liked_users_post_svc,
    likes_post_svc,
    unlikes_post_svc,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, token: str, db: Session = Depends(get_db)):
    user = await get_current_user(token, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized"
        )

    db_post = await create_post_svc(post, user.id, db)
    return db_post


@router.get("/user", response_model=list[Post])
async def get_current_user_posts(token: str, db: Session = Depends(get_db)):
    user = await get_current_user(token, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized"
        )

    posts = await get_users_posts_svc(user.id, db)
    return posts


@router.get("/user/{username}", response_model=list[Post])
async def get_user_posts(username: str, token: str, db: Session = Depends(get_db)):
    user_exists = await existing_user(username, "", db)
    if user_exists:
        user = await get_current_user(token, db)
        user_posts = await get_users_posts_svc(user.id, db)
        return user_posts
    else:
        return []
