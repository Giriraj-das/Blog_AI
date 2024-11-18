from pydantic import BaseModel, EmailStr


class AuthLoginSchema(BaseModel):
    email: EmailStr
    password: str


class AccessRefreshTokensSchema(BaseModel):
    access_token: str
    refresh_token: str | None = None
    type: str = 'Bearer'
