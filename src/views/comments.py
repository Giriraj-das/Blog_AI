from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from crud import CommentCRUD
from models import db_helper
from schemas.comment import CommentSchema, CommentsSchema, CommentCreateSchema, CommentUpdatePartialSchema
from services import CommentService

router = APIRouter(prefix=settings.prefix.comment, tags=['Comments'])


@router.post('', response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
async def create_comment(
        comment_data: CommentCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    comment_service = CommentService(CommentCRUD(session=session))
    return await comment_service.create_comment(comment_data=comment_data)


@router.get('', response_model=list[CommentsSchema])
async def get_comments(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    comment_service = CommentService(CommentCRUD(session=session))
    return await comment_service.get_comments()


@router.get('/{comment_id}', response_model=CommentSchema)
async def get_comment(
        comment_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    comment_service = CommentService(CommentCRUD(session=session))
    return await comment_service.comment_by_id(comment_id=comment_id)


@router.patch("/{comment_id}")
async def update_comment(
        comment_id: int,
        comment_data: CommentUpdatePartialSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    comment_service = CommentService(CommentCRUD(session=session))
    return await comment_service.update_comment(
        comment_id=comment_id,
        comment_data=comment_data,
        partial=True,
    )


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
        comment_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    comment_service = CommentService(CommentCRUD(session=session))
    await comment_service.delete_comment(comment_id=comment_id)
