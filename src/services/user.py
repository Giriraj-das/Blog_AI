import bcrypt
from fastapi import HTTPException, status

from models import User
from crud import UserCRUD
from schemas.user import UserCreateSchema, UserUpdatePartialSchema
from services import BaseService


class UserService(BaseService[UserCRUD]):
    async def create_user(self, user_data: UserCreateSchema):
        user_data.password = self.__hash_password(user_data.password)
        return await self.crud.create_user(user_data=user_data)

    async def get_users(self):
        return await self.crud.get_users()

    async def user_by_id(
            self,
            user_id: int,
    ) -> User:
        user = await self.crud.get_user(user_id=user_id)
        if user:
            return user

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {user_id} not found!",
        )

    async def update_user(
            self,
            user_id: int,
            user_data: UserUpdatePartialSchema,
            partial: bool,
    ):
        user = await self.user_by_id(user_id=user_id)
        if user_data.password:
            user_data.password = self.__hash_password(user_data.password)
        return await self.crud.update_user(user=user, user_data=user_data, partial=partial)

    async def delete_user(self, user_id: int):
        user = await self.user_by_id(user_id=user_id)
        return await self.crud.delete_user(user=user)

    @staticmethod
    def __hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password=password.encode(),
            salt=bcrypt.gensalt()
        ).decode()
