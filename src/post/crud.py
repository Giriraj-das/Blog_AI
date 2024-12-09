from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Post
from post.schemas import PostCreateSchema, PostUpdateSchema, PostUpdatePartialSchema


async def create_post(session: AsyncSession, post_data: PostCreateSchema) -> Post:
    post = Post(**post_data.model_dump())
    session.add(post)
    await session.commit()
    return post


async def get_posts(session: AsyncSession, user_id: int) -> list[Post]:
    stmt = select(Post).where(Post.user_id == user_id).order_by(Post.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_post(session: AsyncSession, user_id: int, post_id: int) -> Post | None:
    stmt = select(Post).where(Post.user_id == user_id, Post.id == post_id)
    result = await session.scalar(stmt)
    return result


async def update_post(
        session: AsyncSession,
        post: Post,
        post_data: PostUpdateSchema | PostUpdatePartialSchema,
        partial: bool = False,
) -> Post:
    for name, value in post_data.model_dump(exclude_unset=partial).items():
        setattr(post, name, value)
    await session.commit()
    return post


async def delete_post(session: AsyncSession, post: Post) -> None:
    await session.delete(post)
    await session.commit()
