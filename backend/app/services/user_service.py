import logging

from app.auth import create_access_token
from app.exceptions import NotFoundError
from app.models.user import User
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository = user_repository

    async def create_user(self, name: str) -> tuple[User, str]:
        """Создаёт пользователя и возвращает его вместе с JWT-токеном."""
        user = await self._repository.create(name)
        token = create_access_token(user.id)
        logger.info("Создан пользователь id=%d name=%s", user.id, user.name)
        return user, token

    async def get_token(self, user_id: int) -> str:
        """Генерирует токен для существующего пользователя."""
        user = await self._get_existing_user(user_id)
        return create_access_token(user.id)

    async def update_name(self, user: User, new_name: str) -> User:
        updated_user = await self._repository.update_name(user, new_name)
        logger.info(
            "Обновлено имя пользователя id=%d: %s",
            updated_user.id,
            updated_user.name,
        )
        return updated_user

    async def delete_user(self, user: User) -> None:
        user_id = user.id
        await self._repository.delete(user)
        logger.info("Удалён пользователь id=%d", user_id)

    async def _get_existing_user(self, user_id: int) -> User:
        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("Пользователь не найден")
        return user
