import logging
from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import decode_access_token
from app.database import async_session_factory
from app.models.user import User
from app.redis import redis_client
from app.repositories.publication_repository import PublicationRepository
from app.repositories.user_repository import UserRepository
from app.services.publication_service import PublicationService
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as session:
        yield session


async def get_redis() -> Redis:
    return redis_client


# --- Репозитории ---

async def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)


async def get_publication_repository(
    session: AsyncSession = Depends(get_session),
) -> PublicationRepository:
    return PublicationRepository(session)


# --- Сервисы ---

async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)


async def get_publication_service(
    publication_repository: PublicationRepository = Depends(
        get_publication_repository
    ),
    redis: Redis = Depends(get_redis),
) -> PublicationService:
    return PublicationService(publication_repository, redis)


# --- Аутентификация ---

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """Извлекает текущего пользователя из JWT-токена."""
    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен авторизации",
        )

    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )
    return user
