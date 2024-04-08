from fastapi import APIRouter

from app.activity.router import router as post_router
from app.auth.router import router as auth_router
from app.post.router import router as activity_router
from app.profile.router import router as profile_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(post_router)
router.include_router(activity_router)
router.include_router(profile_router)
