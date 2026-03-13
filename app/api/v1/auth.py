from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth import get_current_user
from app.core.deps import get_user_service
from app.schemas.auth import UserResponse, UserCreateRequest, TokenResponse, UserLoginRequest, User
from app.services.user_service import UserService

auth_router = APIRouter(tags=["auth"])

@auth_router.post(
    path="/auth/register",
    response_model=UserResponse,
    status_code=201,
    summary="Create a new user",
    description="Creates and stores a new user record."
)
async def create_user(
        body: UserCreateRequest,
        service: UserService = Depends(get_user_service)
) -> UserResponse:
    return service.create_user(body)

@auth_router.post(
    path="/auth/login",
    summary="User login",
    description="Logs the user in.",
    response_model=TokenResponse
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service)
) -> TokenResponse:
    body = UserLoginRequest(
        email=form_data.username,
        password=form_data.password,
    )
    return service.login(body)

@auth_router.get(
    path="/auth/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Determines who the logged-in user is."
)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return UserResponse(
        email=current_user.email,
        is_active=current_user.is_active,
    )