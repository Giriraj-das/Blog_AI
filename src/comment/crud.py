from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Comment
from comment.schemas import CommentCreateSchema, CommentUpdatePartialSchema


async def create_comment(session: AsyncSession, comment_data: CommentCreateSchema) -> Comment:
    comment = Comment(**comment_data.model_dump())
    session.add(comment)
    await session.commit()
    return comment


async def get_comments_by_user(session: AsyncSession, user_id: int) -> list[Comment]:
    stmt = select(Comment).where(Comment.user_id == user_id).order_by(Comment.created_at)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_comment_by_id(session: AsyncSession, comment_id: int) -> Comment | None:
    return await session.get(Comment, comment_id)


async def get_comments_by_post(session: AsyncSession, post_id: int) -> list[Comment]:
    stmt = select(Comment).where(Comment.post_id == post_id)
    result = await session.scalars(stmt)
    return list(result.all())


async def update_comment(
        session: AsyncSession,
        comment: Comment,
        comment_data: CommentUpdatePartialSchema,
        partial: bool = False,
) -> Comment:
    for name, value in comment_data.model_dump(exclude_unset=partial).items():
        setattr(comment, name, value)
    await session.commit()
    return comment


async def delete_comment(session: AsyncSession, comment: Comment) -> None:
    await session.delete(comment)
    await session.commit()
