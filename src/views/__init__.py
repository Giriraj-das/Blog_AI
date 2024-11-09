from fastapi import APIRouter

from .auths import router as auths_router
from .comments import router as comments_router
from .posts import router as posts_router
from .users import router as users_router

router = APIRouter()
router.include_router(router=auths_router)
router.include_router(router=comments_router)
router.include_router(router=posts_router)
router.include_router(router=users_router)
