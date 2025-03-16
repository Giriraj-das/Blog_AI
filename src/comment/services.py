from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from auth.services import get_current_active_auth_user_info
from comment import crud
from core.models import Comment, db_helper
from comment.schemas import CommentCreateRequestSchema, CommentCreateSchema, CommentUpdatePartialSchema
from utils import AuthException


async def create_comment(
        comment_data: CommentCreateRequestSchema,
        user_auth_info: dict = Depends(get_current_active_auth_user_info),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Comment:
    comment_data_with_user = CommentCreateSchema(**comment_data.model_dump(), user_id=user_auth_info['sub'])
    return await crud.create_comment(session=session, comment_data=comment_data_with_user)


async def get_comments_by_user(
        user_auth_info: dict = Depends(get_current_active_auth_user_info),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Comment]:
    return await crud.get_comments_by_user(session=session, user_id=user_auth_info['sub'])


async def get_comments_by_post(
        post_id: int = Path,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Comment]:
    return await crud.get_comments_by_post(session=session, post_id=post_id)


async def get_comment_by_id(
        comment_id: int = Path,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Comment:
    comment: Comment | None = await crud.get_comment_by_id(session=session, comment_id=comment_id)
    if comment:
        return comment
    raise AuthException.not_found(detail=f'Comment {comment_id} not found!')


async def update_comment(
        comment_data: CommentUpdatePartialSchema,
        comment: Comment = Depends(get_comment_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_comment(session=session, comment=comment, comment_data=comment_data, partial=True)


async def delete_comment(
        comment: Comment = Depends(get_comment_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_comment(session=session, comment=comment)
