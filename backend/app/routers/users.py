from fastapi import APIRouter, Depends, status

from app.dependencies import get_current_user, get_user_service
from app.models.user import User
from app.schemas.user import (
    TokenResponse,
    UserCreate,
    UserCreateResponse,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    body: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserCreateResponse:
    user, token = await user_service.create_user(body.name)
    return UserCreateResponse(
        user=UserResponse.model_validate(user),
        access_token=token,
    )


@router.get("/{user_id}/token", response_model=TokenResponse)
async def get_user_token(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> TokenResponse:
    token = await user_service.get_token(user_id)
    return TokenResponse(access_token=token)


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    body: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    updated = await user_service.update_name(current_user, body.name)
    return UserResponse.model_validate(updated)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> None:
    await user_service.delete_user(current_user)
