from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class UserUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class UserCreateResponse(BaseModel):
    user: UserResponse
    access_token: str


class TokenResponse(BaseModel):
    access_token: str
