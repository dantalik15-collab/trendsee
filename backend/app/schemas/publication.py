from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PublicationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    text: str = Field(min_length=1)


class PublicationUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    text: str | None = Field(default=None, min_length=1)


class PublicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    text: str
    created_at: datetime
    updated_at: datetime


class PublicationListResponse(BaseModel):
    items: list[PublicationResponse]
    total: int
    has_more: bool
