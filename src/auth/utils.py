import bcrypt
import jwt

from config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.encode(payload=payload, key=private_key, algorithm=algorithm)


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


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode()
    )
