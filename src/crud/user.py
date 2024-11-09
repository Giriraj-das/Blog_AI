from sqlalchemy import select

from crud.base import BaseCRUD
from models import User
from schemas.user import UserCreateSchema, UserUpdateSchema, UserUpdatePartialSchema


class UserCRUD(BaseCRUD):
    async def create_user(self, user_data: UserCreateSchema) -> User:
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_users(self) -> list[User]:
        stmt = select(User).order_by(User.id)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_user(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return await self.session.scalar(stmt)

    async def update_user(
            self,
            user: User,
            user_data: UserUpdateSchema | UserUpdatePartialSchema,
            partial: bool = False,
    ) -> User:
        for name, value in user_data.model_dump(exclude_unset=partial).items():
            setattr(user, name, value)
        await self.session.commit()
        return user

    async def delete_user(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
