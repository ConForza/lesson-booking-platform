from app.core.exceptions import DomainError
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreateRequest, UserLoginRequest, User, UserResponse
from app.core.security import hash_password

class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, body: UserCreateRequest) -> UserResponse:
        if body.email.strip() == "":
            raise DomainError("Email must not be left blank")

        if self.user_repo.get_user_by_email(body.email) is not None:
            raise DomainError("User already exists", status_code=400)

        if len(body.password) < 8:
            raise DomainError("Password must be at least 8 characters")

        user = User(
            email=body.email,
            password=hash_password(body.password),
            is_active=True,
        )

        self.user_repo.create_user(user)

        return UserResponse(
            email=body.email,
            is_active=user.is_active,
        )