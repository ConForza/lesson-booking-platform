from fastapi.security import OAuth2PasswordBearer

from fastapi import Depends
from app.core.jwt import decode_access_token
from app.core.exceptions import DomainError
from app.core.deps import get_user_repository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_repo: UserRepository = Depends(get_user_repository)
) -> User:
    payload = decode_access_token(token)

    if payload is None:
        raise DomainError("Invalid authentication credentials", status_code=401)

    email = payload.get("sub")

    if email is None:
        raise DomainError("Invalid authentication credentials", status_code=401)

    user = user_repo.get_user_by_email(email)

    if user is None:
        raise DomainError("User not found", status_code=401)

    return user