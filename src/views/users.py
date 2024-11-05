from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from crud import UserCRUD
from models import db_helper
from schemas.user import UserSchema, UsersSchema, UserCreateSchema, UserUpdatePartialSchema
from services import UserService

router = APIRouter(prefix=settings.prefix.user, tags=['Users'])


@router.post('', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: UserCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user_service = UserService(UserCRUD(session=session))
    return await user_service.create_user(user_data=user_data)


@router.get('', response_model=list[UsersSchema])
async def get_users(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user_service = UserService(UserCRUD(session=session))
    return await user_service.get_users()


@router.get('/{user_id}', response_model=UserSchema)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user_service = UserService(UserCRUD(session=session))
    return await user_service.user_by_id(user_id=user_id)


@router.patch("/{user_id}")
async def update_user(
        user_id: int,
        user_data: UserUpdatePartialSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user_service = UserService(UserCRUD(session=session))
    return await user_service.update_user(
        user_id=user_id,
        user_data=user_data,
        partial=True,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    user_service = UserService(UserCRUD(session=session))
    await user_service.delete_user(user_id=user_id)
