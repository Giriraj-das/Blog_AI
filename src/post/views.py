from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.services import get_current_active_auth_user_info
from core.config import settings
from core.models import db_helper, Post
from post.schemas import PostSchema, PostsSchema, PostUpdatePartialSchema
from post import services

router = APIRouter(prefix=settings.prefix.post, tags=['Posts'])


@router.post('', response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
        post: Post = Depends(services.create_post)
):
    return post


@router.get('', response_model=list[PostsSchema])
async def get_posts(
        posts: list[Post] = Depends(services.get_posts),
):
    return posts


@router.get('/{post_id}', response_model=PostSchema)
async def get_post(
        post: Post = Depends(services.get_post)
):
    return post


@router.patch('/{post_id}')
async def update_post(
        post: Post = Depends(services.update_post)
):
    return post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(services.delete_post)],
)
async def delete_post() -> None:
    pass
