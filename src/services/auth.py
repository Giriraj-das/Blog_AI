import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException, status

from config import settings
from crud import UserCRUD
from schemas.auth import AuthLoginSchema, TokensInfoSchema
from schemas.user import UserSchema, UserCreateSchema
from services import BaseService


class AuthService(BaseService[UserCRUD]):

    async def register(self, reg_data: UserCreateSchema):
        reg_data.password = self.__hash_password(reg_data.password)
        return await self.crud.create_user(user_data=reg_data)

    async def login(self, login_data: AuthLoginSchema):
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password',
        )
        if not (user := await self.crud.get_user_by_email(login_data.email)):
            raise unauthed_exc
        if not self.__compare_password(
                password=login_data.password,
                hashed_password=user.password,
        ):
            raise unauthed_exc
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User inactive",
            )

        access_token = self.__create_access_token(user)
        refresh_token = self.__create_refresh_token(user)
        return TokensInfoSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def __create_access_token(self, user: UserSchema) -> str:
        payload = {
            'sub': user.id,
            'username': user.username,
            'email': user.email,
            'type': 'access',
        }
        return self.__encode_jwt(
            payload=payload,
            expire_minutes=settings.auth_jwt.access_token_expire_minutes,
        )

    def __create_refresh_token(self, user: UserSchema) -> str:
        payload = {
            "sub": user.id,
            "username": user.username,
            'type': 'refresh',
        }
        return self.__encode_jwt(
            payload=payload,
            expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
        )

    @staticmethod
    def __hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password=password.encode(),
            salt=bcrypt.gensalt()
        ).decode()

    @staticmethod
    def __compare_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password.encode()
        )

    @staticmethod
    def __encode_jwt(
            payload: dict,
            private_key: str = settings.auth_jwt.private_key_path.read_text(),
            algorithm: str = settings.auth_jwt.algorithm,
            expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
            expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(exp=expire, iat=now, jti=str(uuid.uuid4()))
        return jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)

    @staticmethod
    def __decode_jwt(
            token: str | bytes,
            public_key: str = settings.auth_jwt.public_key_path.read_text(),
            algorithm: str = settings.auth_jwt.algorithm,
    ):
        return jwt.decode(token, public_key, algorithms=[algorithm])
