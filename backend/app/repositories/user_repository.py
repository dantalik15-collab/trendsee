from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, name: str) -> User:
        user = User(name=name)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)

    async def update_name(
        self, user: User, new_name: str
    ) -> User:
        user.name = new_name
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self._session.delete(user)
        await self._session.commit()

    async def exists(self, user_id: int) -> bool:
        query = select(User.id).where(User.id == user_id)
        result = await self._session.execute(query)
        return result.scalar_one_or_none() is not None
