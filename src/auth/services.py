from datetime import timedelta
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from auth.schemas import AuthLoginSchema, AccessRefreshTokensSchema
from core.models import db_helper, User
from user import crud as user_crud
from user.schemas import UserCreateSchema
from utils import AuthException, hash_password, compare_password, encode_jwt, decode_jwt

http_bearer = HTTPBearer()

ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token: str = credentials.credentials
    try:
        payload: dict = decode_jwt(token=token)
    except ExpiredSignatureError:
        raise AuthException.unauthorized(detail='Token has expired')
    except InvalidTokenError:
        raise AuthException.unauthorized(detail='Invalid token error')
    return payload


async def get_user_by_token_sub(
        payload: dict,
        session: AsyncSession,
) -> User:
    user_id: int | None = payload.get('sub')
    user: User | None = await user_crud.get_user(session=session, user_id=user_id)
    if not user:
        raise AuthException.unauthorized(detail='Token invalid')
    if not user.is_active:
        raise AuthException.forbidden(detail='User inactive')
    return user


def validate_token_type(
        payload: dict,
        token_type: str,
) -> None:
    current_token_type: str | None = payload.get('type')
    if current_token_type != token_type:
        raise AuthException.unauthorized(
            detail=f'Invalid token type {current_token_type!r} expected {token_type!r}'
        )


async def get_current_active_auth_user_info(
        payload: dict = Depends(get_current_token_payload),
) -> dict:
    validate_token_type(payload=payload, token_type=ACCESS_TOKEN_TYPE)
    return payload


async def generate_access_token_by_refresh(
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> AccessRefreshTokensSchema:
    validate_token_type(payload=payload, token_type=REFRESH_TOKEN_TYPE)
    user = await get_user_by_token_sub(payload=payload, session=session)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return AccessRefreshTokensSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def register(
        reg_data: UserCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    reg_data.password = hash_password(reg_data.password)

    if await user_crud.is_user_exists(session, reg_data.username, reg_data.email):
        raise AuthException.bad_request(detail='A user with this username or email already exists')

    user = await user_crud.create_user(session=session, user_data=reg_data)
    return user


async def login_user_validator(
        login_data: AuthLoginSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    user: User | None = await user_crud.get_user_by_email(session=session, email=login_data.email)
    if not user:
        raise AuthException.unauthorized(detail='Invalid email or password')
    if not compare_password(
            new_password=login_data.password,
            old_password=user.password,
    ):
        raise AuthException.unauthorized(detail='Invalid email or password')
    if not user.is_active:
        raise AuthException.forbidden(detail='User inactive')
    return user


def login_user(
        user: User = Depends(login_user_validator)
) -> AccessRefreshTokensSchema:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return AccessRefreshTokensSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


def create_access_token(user: User) -> str:
    access_payload = {
        'sub': user.id,
        'username': user.username,
        'email': user.email,
        'type': ACCESS_TOKEN_TYPE,
    }
    return encode_jwt(
        payload=access_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: User) -> str:
    refresh_payload = {
        'sub': user.id,
        'username': user.username,
        'type': REFRESH_TOKEN_TYPE,
    }
    return encode_jwt(
        payload=refresh_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
