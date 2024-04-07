from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.post.router import router as post_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(post_router)
