from fastapi import APIRouter, Depends, Query, status

from app.dependencies import get_current_user, get_publication_service
from app.models.user import User
from app.schemas.publication import (
    PublicationCreate,
    PublicationListResponse,
    PublicationResponse,
    PublicationUpdate,
)
from app.services.publication_service import PublicationService

router = APIRouter(prefix="/publications", tags=["Publications"])

DEFAULT_PAGE_LIMIT = 20
MAX_PAGE_LIMIT = 100


@router.post(
    "",
    response_model=PublicationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_publication(
    body: PublicationCreate,
    current_user: User = Depends(get_current_user),
    publication_service: PublicationService = Depends(
        get_publication_service
    ),
) -> PublicationResponse:
    publication = await publication_service.create_publication(
        user_id=current_user.id,
        title=body.title,
        text=body.text,
    )
    return PublicationResponse.model_validate(publication)


@router.get("", response_model=PublicationListResponse)
async def get_publications(
    user_id: int | None = Query(default=None, description="Фильтр по автору"),
    limit: int = Query(
        default=DEFAULT_PAGE_LIMIT, ge=1, le=MAX_PAGE_LIMIT
    ),
    offset: int = Query(default=0, ge=0),
    publication_service: PublicationService = Depends(
        get_publication_service
    ),
) -> PublicationListResponse:
    items, total, has_more = await publication_service.get_publications(
        limit=limit, offset=offset, user_id=user_id
    )
    return PublicationListResponse(
        items=items, total=total, has_more=has_more
    )


@router.get("/{publication_id}", response_model=PublicationResponse)
async def get_publication(
    publication_id: int,
    publication_service: PublicationService = Depends(
        get_publication_service
    ),
) -> PublicationResponse:
    return await publication_service.get_publication(publication_id)


@router.patch(
    "/{publication_id}", response_model=PublicationResponse
)
async def update_publication(
    publication_id: int,
    body: PublicationUpdate,
    current_user: User = Depends(get_current_user),
    publication_service: PublicationService = Depends(
        get_publication_service
    ),
) -> PublicationResponse:
    publication = await publication_service.update_publication(
        publication_id=publication_id,
        current_user_id=current_user.id,
        title=body.title,
        text=body.text,
    )
    return PublicationResponse.model_validate(publication)


@router.delete(
    "/{publication_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_publication(
    publication_id: int,
    current_user: User = Depends(get_current_user),
    publication_service: PublicationService = Depends(
        get_publication_service
    ),
) -> None:
    await publication_service.delete_publication(
        publication_id=publication_id,
        current_user_id=current_user.id,
    )
