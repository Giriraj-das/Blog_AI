from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from user.schemas import UserCreateSchema, UserUpdateSchema, UserUpdatePartialSchema


async def create_user(session: AsyncSession, user_data: UserCreateSchema) -> User:
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return await session.scalar(stmt)


async def update_user(
        session: AsyncSession,
        user: User,
        user_data: UserUpdateSchema | UserUpdatePartialSchema,
        partial: bool = False,
) -> User:
    for name, value in user_data.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()


async def is_user_exists(session: AsyncSession, username: str, email: str) -> bool:
    stmt = select(User).where(
        or_(User.username == username, User.email == email)
    )
    result = await session.scalar(stmt)
    return result is not None
