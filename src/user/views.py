from fastapi import APIRouter, status, Depends

from core.config import settings
from core.models import User
from user.schemas import UserSchema, UsersSchema, UserUpdatePartialSchema
from user import services

router = APIRouter(prefix=settings.prefix.user, tags=['Users'])


@router.get('', response_model=list[UsersSchema])
async def get_users(
        users: list[User] = Depends(services.get_users)
):
    return users


@router.get('/{user_id}', response_model=UserSchema)
async def get_user(
        user: User = Depends(services.user_by_id)
):
    return user


@router.patch('/{user_id}')
async def update_user(
        user: User = Depends(services.update_user)
):
    return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user: User = Depends(services.delete_user),
) -> None:
    pass
