import re
from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.auth.models import User
from app.post.models import Hashtag, Post, post_hashtags
from app.post.schemas import Post as PostSchema
from app.post.schemas import PostCreate


async def get_posts_by_username(username: str, db: Session) -> List[Post]:
    return db.query(Post).filter(Post.author.has(username=username)).all()


async def create_hashtags_svc(post: Post, db: Session):
    regex = r"#\w+"
    matches = re.findall(regex, post.content)

    for match in matches:
        name = match[1:]

        hashtag = db.query(Hashtag).filter(Hashtag.name == name).first()
        if not hashtag:
            hashtag = Hashtag(name=name)
            db.add(hashtag)
            db.commit()
        post.hashtags.append(hashtag)

    db.commit()


async def create_post_svc(post: PostCreate, user_id: int, db: Session):
    db_post = Post(
        content=post.content,
        image=post.image,
        location=post.location,
        author_id=user_id,
    )

    await create_hashtags_svc(db_post, db)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


async def get_users_posts_svc(user_id: int, db: Session) -> list[PostSchema]:
    posts = (
        db.query(Post)
        .filter(Post.author_id == user_id)
        .order_by(desc(Post.created_dt))
        .all()
    )

    return posts


async def get_posts_from_hashtag_svc(hashtag_name: str, db: Session):
    hashtag = db.query(Hashtag).filter(Hashtag.name == hashtag_name).first()
    if not hashtag:
        return None
    return hashtag.posts


async def get_random_posts_svc(
    db: Session, page: int = 1, limit: int = 10, hashtag: str = None
):
    total_posts = db.query(Post).count()

    offset = (page - 1) * limit
    if offset >= total_posts:
        return []

    posts = db.query(Post, User.username).join(User).order_by(desc(Post.created_dt))

    if hashtag:
        posts = posts.join(post_hashtags).join(Hashtag).filter(Hashtag.name == hashtag)

    posts = posts.offset(offset).limit(limit).all()

    result = []
    for post, username in posts:
        post_dict = post.__dict__
        post_dict["username"] = username
        result.append(post_dict)

    return result


async def get_post_from_post_id_svc(post_id: int, db: Session) -> PostSchema:
    return db.query(Post).filter(Post.id == post_id).first()


async def delete_post_svc(post_id: int, db: Session):
    post = await get_post_from_post_id_svc(post_id, db)
    db.delete(post)
    db.commit()


async def like_post_svc(post_id: int, username: str, db: Session):
    post = await get_post_from_post_id_svc(post_id, db)

    if not post:
        return False, "Invalid post_id"

    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False, "Invalid username"

    if user in post.like_by_users:
        return False, "Already Liked"

    post.like_by_users.append(user)
    post.likes_count = len(post.like_by_users)

    db.commit()
    return True, "done"


async def unlike_post_svc(post_id: int, username: str, db: Session):
    post = await get_post_from_post_id_svc(post_id, db)

    if not post:
        return False, "Invalid post_id"

    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False, "Invalid username"

    if not user in post.like_by_users:
        return False, "Already Not Liked"

    post.like_by_users.remove(user)
    post.likes_count = len(post.like_by_users)

    db.commit()


async def liked_users_post_svc(post_id: int, db: Session) -> List[User]:
    post = await get_post_from_post_id_svc(post_id, db)

    if not post:
        return []
    liked_users = post.like_by_users
    return liked_users
