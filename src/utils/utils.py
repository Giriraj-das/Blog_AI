import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from core.config import settings


def encode_jwt(
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


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.decode(token, public_key, algorithms=[algorithm])


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password=password.encode(),
        salt=bcrypt.gensalt()
    ).decode()


def compare_password(new_password: str, old_password: str) -> bool:
    return bcrypt.checkpw(
        password=new_password.encode(),
        hashed_password=old_password.encode()
    )
