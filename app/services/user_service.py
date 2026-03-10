from app.core.exceptions import DomainError
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserCreateRequest, UserLoginRequest, User, UserResponse
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

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

    def login(self, body: UserLoginRequest):

        user = self.user_repo.get_user_by_email(body.email)

        if user is None:
            raise DomainError("Invalid email or password", status_code=401)

        if not verify_password(body.password, user.password):
            raise DomainError("Invalid email or password", status_code=401)

        token = create_access_token(
            data={"sub": user.email}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }