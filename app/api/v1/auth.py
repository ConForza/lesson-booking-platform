from fastapi import APIRouter, Depends

from app.core.deps import get_user_service
from app.schemas.auth import UserResponse, UserCreateRequest
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