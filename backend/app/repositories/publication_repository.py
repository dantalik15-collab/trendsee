import asyncio
import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.publication import Publication

logger = logging.getLogger(__name__)

# Имитация нагрузки при чтении из Postgres
DATABASE_READ_DELAY_SECONDS = 2


class PublicationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: int, title: str, text: str) -> Publication:
        publication = Publication(
            user_id=user_id,
            title=title,
            text=text,
        )
        self._session.add(publication)
        await self._session.commit()
        await self._session.refresh(publication)
        return publication

    async def get_by_id(self, publication_id: int) -> Publication | None:
        """Получение публикации из Postgres с искусственной задержкой."""
        logger.debug(
            "Чтение публикации id=%d из Postgres (задержка %d сек)",
            publication_id,
            DATABASE_READ_DELAY_SECONDS,
        )
        await asyncio.sleep(DATABASE_READ_DELAY_SECONDS)
        return await self._session.get(Publication, publication_id)

    async def get_list(
        self,
        limit: int,
        offset: int,
        user_id: int | None = None,
    ) -> list[Publication]:
        """Получение списка публикаций с пагинацией и опциональным фильтром.

        Args:
            limit: Максимальное количество записей.
            offset: Смещение от начала.
            user_id: Если указан — только публикации этого автора.
        """
        logger.debug(
            "Чтение списка публикаций из Postgres (задержка %d сек)",
            DATABASE_READ_DELAY_SECONDS,
        )
        await asyncio.sleep(DATABASE_READ_DELAY_SECONDS)

        query = select(Publication).order_by(Publication.created_at.desc())
        if user_id is not None:
            query = query.where(Publication.user_id == user_id)
        query = query.limit(limit).offset(offset)

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def count(self, user_id: int | None = None) -> int:
        query = select(func.count(Publication.id))
        if user_id is not None:
            query = query.where(Publication.user_id == user_id)
        result = await self._session.execute(query)
        return result.scalar_one()

    async def update(
        self,
        publication: Publication,
        title: str | None = None,
        text: str | None = None,
    ) -> Publication:
        if title is not None:
            publication.title = title
        if text is not None:
            publication.text = text
        await self._session.commit()
        await self._session.refresh(publication)
        return publication

    async def delete(self, publication: Publication) -> None:
        await self._session.delete(publication)
        await self._session.commit()

    async def get_by_id_no_delay(
        self, publication_id: int
    ) -> Publication | None:
        """Получение без задержки — для update/delete операций."""
        return await self._session.get(Publication, publication_id)
