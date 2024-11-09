from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from crud import UserCRUD
from models import db_helper
from schemas.auth import TokensInfoSchema, AuthLoginSchema
from schemas.user import UserSchema, UserCreateSchema
from services import AuthService

router = APIRouter(prefix=settings.prefix.auth, tags=['Auths'])


@router.post('/register', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register(
        user_data: UserCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    auth_service = AuthService(UserCRUD(session=session))
    return await auth_service.register(reg_data=user_data)


@router.post('/login', response_model=TokensInfoSchema)
async def login(
        login_data: AuthLoginSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    auth_service = AuthService(UserCRUD(session=session))
    return await auth_service.login(login_data)


# @router.post("/refresh/",
#     response_model=TokenInfo,
#     response_model_exclude_none=True,
# )
# def auth_refresh_jwt(
#     # todo: validate user is active!!
#     user: UserSchema = Depends(get_current_auth_user_for_refresh),
#     # user: UserSchema = Depends(get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)),
#     # user: UserSchema = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE)),
# ):
#     access_token = create_access_token(user)
#     return TokenInfo(
#         access_token=access_token,
#     )


# @router.get("/me")
# def check_self_info(
#     payload: dict = Depends(get_current_token_payload),
#     user: UserSchema = Depends(get_current_active_auth_user),
# ):
#     iat = payload.get("iat")
#     return {
#         "username": user.username,
#         "email": user.email,
#         "logged_in_at": iat,
#     }
