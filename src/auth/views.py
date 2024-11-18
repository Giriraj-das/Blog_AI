from fastapi import APIRouter, Depends, status

from auth.schemas import AccessRefreshTokensSchema
from core.config import settings
from core.models import User
from user.schemas import UserSchema
from auth import services

router = APIRouter(prefix=settings.prefix.auth, tags=['Auths'])


@router.post('/register', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register(
        user: User = Depends(services.register)
):
    return user


@router.post('/login', response_model=AccessRefreshTokensSchema)
async def login(
        schema: AccessRefreshTokensSchema = Depends(services.login_user),
):
    return schema


@router.get("/me")
async def auth_user_check_self_info(
        auth_info: dict = Depends(services.get_current_active_auth_user_info),
):
    return auth_info


@router.post("/refresh", response_model=AccessRefreshTokensSchema)
def refresh_jwt(
    schema: AccessRefreshTokensSchema = Depends(services.generate_access_token_by_refresh),
):
    return schema
