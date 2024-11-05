from fastapi import APIRouter

from .users import router as users_router
# from .posts import router as posts_router
# from .comments import router as comments_router

router = APIRouter()
router.include_router(router=users_router)
# router.include_router(router=posts_router)
# router.include_router(router=comments_router)
