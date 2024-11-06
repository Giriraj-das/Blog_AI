from datetime import datetime
from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(UserCreateSchema):
    pass


class UserUpdatePartialSchema(UserCreateSchema):
    username: Annotated[str, MinLen(3), MaxLen(20)] | None = None
    email: EmailStr | None = None
    password: str | None = None


class UsersSchema(UserBaseSchema):
    id: int


class UserSchema(UsersSchema):
    is_active: bool = True
    created_at: datetime
