from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from auth.services import get_current_active_auth_user_info
from core.models import Post, db_helper
from post import crud
from post.schemas import PostCreateRequestSchema, PostCreateSchema, PostUpdatePartialSchema
from utils import AuthException


async def create_post(
        post_data: PostCreateRequestSchema,
        user_auth_info: dict = Depends(get_current_active_auth_user_info),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Post:
    post_data_with_user: PostCreateSchema = PostCreateSchema(**post_data.dict(), user_id=user_auth_info['sub'])
    return await crud.create_post(session=session, post_data=post_data_with_user)


async def get_posts(
        user_auth_info: dict = Depends(get_current_active_auth_user_info),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Post]:
    return await crud.get_posts(session=session, user_id=user_auth_info['sub'])


async def get_post(
        post_id: int = Path,
        user_auth_info: dict = Depends(get_current_active_auth_user_info),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Post:
    post: Post | None = await crud.get_post(session=session, user_id=user_auth_info['sub'], post_id=post_id)
    if post:
        return post
    raise AuthException.not_found(detail=f'Post {post_id} not found!')


async def update_post(
        post_data: PostUpdatePartialSchema,
        post: Post = Depends(get_post),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Post:
    return await crud.update_post(session=session, post=post, post_data=post_data, partial=True)


async def delete_post(
        post: Post = Depends(get_post),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_post(session=session, post=post)
