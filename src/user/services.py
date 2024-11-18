from fastapi import HTTPException, status, Depends, Path

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from user import crud as user_crud
from user.schemas import UserUpdatePartialSchema
from utils import hash_password


async def get_users(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[User]:
    return await user_crud.get_users(session=session)


async def user_by_id(
        user_id: int = Path,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    user: User | None = await user_crud.get_user(session=session, user_id=user_id)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )


async def update_user(
        user_data: UserUpdatePartialSchema,
        user: User = Depends(user_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    if user_data.password:
        user_data.password = hash_password(user_data.password)
    return await user_crud.update_user(
        session=session, user=user, user_data=user_data, partial=True
    )


async def delete_user(
        user: User = Depends(user_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await user_crud.delete_user(session=session, user=user)
