from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.schemas import User
from app.auth.service import existing_user, get_current_user
from app.core.db import get_db
from app.post.schemas import Post, PostCreate
from app.post.service import (
    create_post_svc,
    delete_post_svc,
    get_post_from_post_id_svc,
    get_posts_by_username,
    get_posts_from_hashtag_svc,
    get_random_posts_svc,
    get_users_posts_svc,
    like_post_svc,
    liked_users_post_svc,
    unlike_post_svc,
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
async def get_user_posts(username: str, db: Session = Depends(get_db)):
    user_exists = await existing_user(username, "", db)
    if user_exists:
        user_posts = await get_posts_by_username(username, db)
        return user_posts
    else:
        return []


@router.get("/hashtag/{hashtag}")
async def get_posts_from_hashtag(hashtag: str, db: Session = Depends(get_db)):
    posts = await get_posts_from_hashtag_svc(hashtag, db)
    return posts


@router.get("/feed")
async def get_random_posts(
    db: Session = Depends(get_db), page: int = 1, limit: int = 10, hashtag: str = None
):
    return await get_random_posts_svc(db, page, limit, hashtag)


@router.delete("/")
async def delete_post(token: str, post_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(token, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized"
        )

    post = await get_post_from_post_id_svc(post_id, db)
    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized"
        )

    await delete_post_svc(post_id, db)


@router.get("/like", status_code=status.HTTP_204_NO_CONTENT)
async def like_post(post_id: int, username: str, db: Session = Depends(get_db)):
    res, detail = await like_post_svc(post_id, username, db)
    if res == False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.get("/unlike", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_post(post_id: int, username: str, db: Session = Depends(get_db)):
    res, detail = await unlike_post_svc(post_id, username, db)
    if res == False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.get("likes/{post_id}", response_model=list[User])
async def users_like_post(post_id: int, db: Session = Depends(get_db)):
    return await liked_users_post_svc(post_id, db)


@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = await get_post_from_post_id_svc(post_id, db)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invaild post id"
        )

    return db_post
