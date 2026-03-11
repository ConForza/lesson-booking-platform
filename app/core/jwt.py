from datetime import datetime, timedelta, timezone
import jwt

from app.core.config import get_settings

settings = get_settings()

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.algorithm]
        )
        return payload
    except jwt.PyJWTError:
        return None