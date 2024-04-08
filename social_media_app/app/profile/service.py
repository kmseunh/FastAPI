from sqlalchemy.orm import Session

from app.activity.models import Activity
from app.auth.models import Follow, User
from app.auth.service import existing_user, get_user_by_user_id, get_user_by_username
from app.profile.schemas import FollowerList, FollowingList


async def follow_svc(db: Session, follower: str, following: str):
    db_follower_exist = await existing_user(follower, "", db)
    db_following_exist = await existing_user(following, "", db)

    if not db_follower_exist or not db_following_exist:
        return False

    db_follower = await get_user_by_username(follower, db)
    db_following = await get_user_by_username(following, db)

    db_follow = (
        db.query(Follow)
        .filter_by(follower_id=db_follower.id, following_id=db_following.id)
        .first()
    )

    if db_follow:
        return False

    db_follow = Follow(follower_id=db_follower.id, following_id=db_following.id)
    db.add(db_follow)

    db_follower.followings_count += 1
    db_following.followers_count += 1

    follow_activity = Activity(
        username=db_following.username,
        followed_username=db_follower.username,
        followed_user_pic=db_follower.profile_pic,
    )

    db.add(follow_activity)
    db.commit()
    db.refresh(follow_activity)


async def unfollow_svc(db: Session, follower: str, following: str):
    db_follower_exist = await existing_user(follower, "", db)
    db_following_exist = await existing_user(following, "", db)

    if not db_follower_exist or not db_following_exist:
        return False

    db_follower = await get_user_by_username(follower, db)
    db_following = await get_user_by_username(following, db)

    db_follow = (
        db.query(Follow)
        .filter_by(follower_id=db_follower.id, following_id=db_following.id)
        .first()
    )

    if not db_follow:
        return False

    db.delete(db_follow)

    db_follower.followings_count -= 1
    db_following.followers_count -= 1

    db.commit()


async def get_followers_svc(db: Session, user_id: int) -> list[FollowerList]:
    db_user = await get_user_by_user_id(db, user_id)

    if not db_user:
        return []

    db_followers = (
        db.query(Follow)
        .filter_by(following_id=user_id)
        .join(User, User.id == Follow.follower_id)
        .all()
    )

    followers = []
    for user in db_followers:
        followers.append(
            {
                "profile_pic": user.follower.profie_pic,
                "name": user.follower.name,
                "username": user.follower.username,
            }
        )

    return FollowerList(followers=followers)


async def get_followings_svc(db: Session, user_id: int) -> list[FollowingList]:
    db_user = await get_user_by_user_id(db, user_id)

    if not db_user:
        return []

    db_followings = (
        db.query(Follow)
        .filter_by(follower_id=user_id)
        .join(User, User.id == Follow.following_id)
        .all()
    )

    following = []
    for user in db_followings:
        following.append(
            {
                "profile_pic": user.follower.profile_pic,
                "name": user.follower.name,
                "username": user.follower.username,
            }
        )

    return FollowingList(followings=following)
