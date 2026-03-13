import json
import logging
from datetime import datetime

from redis.asyncio import Redis

from app.exceptions import ForbiddenError, NotFoundError
from app.models.publication import Publication
from app.repositories.publication_repository import PublicationRepository
from app.schemas.publication import PublicationResponse

logger = logging.getLogger(__name__)

# TTL для "горячих" публикаций в Redis
PUBLICATION_CACHE_TTL_SECONDS = 600

# Префикс ключей в Redis
CACHE_KEY_PREFIX = "publication"


def _cache_key(publication_id: int) -> str:
    return f"{CACHE_KEY_PREFIX}:{publication_id}"


def _serialize_publication(publication: Publication) -> str:
    """Сериализация SQLAlchemy-модели в JSON для Redis."""
    return json.dumps(
        {
            "id": publication.id,
            "user_id": publication.user_id,
            "title": publication.title,
            "text": publication.text,
            "created_at": publication.created_at.isoformat(),
            "updated_at": publication.updated_at.isoformat(),
        }
    )


def _deserialize_publication(data: str) -> PublicationResponse:
    """Десериализация JSON из Redis в Pydantic-схему."""
    parsed = json.loads(data)
    return PublicationResponse(
        id=parsed["id"],
        user_id=parsed["user_id"],
        title=parsed["title"],
        text=parsed["text"],
        created_at=datetime.fromisoformat(parsed["created_at"]),
        updated_at=datetime.fromisoformat(parsed["updated_at"]),
    )


class PublicationService:
    def __init__(
        self,
        publication_repository: PublicationRepository,
        redis: Redis,
    ) -> None:
        self._repository = publication_repository
        self._redis = redis

    async def create_publication(
        self,
        user_id: int,
        title: str,
        text: str,
    ) -> Publication:
        publication = await self._repository.create(user_id, title, text)

        # Кладём в Redis как "горячую" публикацию
        await self._cache_publication(publication)

        logger.info(
            "Создана публикация id=%d автор=%d",
            publication.id,
            publication.user_id,
        )
        return publication

    async def get_publication(
        self, publication_id: int
    ) -> PublicationResponse:
        """Сначала ищем в Redis, при промахе — в Postgres с задержкой."""
        cached = await self._get_from_cache(publication_id)
        if cached is not None:
            logger.debug(
                "Публикация id=%d отдана из Redis", publication_id
            )
            return cached

        publication = await self._repository.get_by_id(publication_id)
        if publication is None:
            raise NotFoundError("Публикация не найдена")

        logger.debug(
            "Публикация id=%d отдана из Postgres", publication_id
        )
        return PublicationResponse.model_validate(publication)

    async def get_publications(
        self,
        limit: int,
        offset: int,
        user_id: int | None = None,
    ) -> tuple[list[PublicationResponse], int, bool]:
        """Возвращает список публикаций, общее количество и флаг has_more."""
        publications = await self._repository.get_list(
            limit=limit, offset=offset, user_id=user_id
        )
        total = await self._repository.count(user_id=user_id)
        has_more = (offset + limit) < total

        items = [
            PublicationResponse.model_validate(pub)
            for pub in publications
        ]
        return items, total, has_more

    async def update_publication(
        self,
        publication_id: int,
        current_user_id: int,
        title: str | None = None,
        text: str | None = None,
    ) -> Publication:
        publication = await self._get_owned_publication(
            publication_id, current_user_id
        )
        updated = await self._repository.update(publication, title, text)

        # Инвалидируем кэш — данные изменились
        await self._invalidate_cache(publication_id)

        logger.info("Обновлена публикация id=%d", publication_id)
        return updated

    async def delete_publication(
        self,
        publication_id: int,
        current_user_id: int,
    ) -> None:
        publication = await self._get_owned_publication(
            publication_id, current_user_id
        )
        await self._repository.delete(publication)
        await self._invalidate_cache(publication_id)

        logger.info("Удалена публикация id=%d", publication_id)

    # --- Приватные методы ---

    async def _get_owned_publication(
        self,
        publication_id: int,
        current_user_id: int,
    ) -> Publication:
        """Получает публикацию и проверяет что текущий юзер — автор."""
        publication = await self._repository.get_by_id_no_delay(
            publication_id
        )
        if publication is None:
            raise NotFoundError("Публикация не найдена")
        if publication.user_id != current_user_id:
            raise ForbiddenError("Нет прав на изменение этой публикации")
        return publication

    async def _cache_publication(self, publication: Publication) -> None:
        key = _cache_key(publication.id)
        value = _serialize_publication(publication)
        await self._redis.set(key, value, ex=PUBLICATION_CACHE_TTL_SECONDS)

    async def _get_from_cache(
        self, publication_id: int
    ) -> PublicationResponse | None:
        key = _cache_key(publication_id)
        data = await self._redis.get(key)
        if data is None:
            return None
        return _deserialize_publication(data)

    async def _invalidate_cache(self, publication_id: int) -> None:
        key = _cache_key(publication_id)
        await self._redis.delete(key)
