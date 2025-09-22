from typing import Sequence
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.domain.models.user import User

class UserRepository:
    async def create_user(self, user: User, session: AsyncSession) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_all_users(self, session: AsyncSession) -> Sequence[User]:
        result = await session.exec(select(User))
        return result.all()

    async def get_user_by_id(self, user_id: int, session: AsyncSession) -> User | None:
        return await session.get(User, user_id)

    async def update_user(self, user: User, session: AsyncSession) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def delete_user(self, user_id: int, session: AsyncSession) -> bool:
        user = await session.get(User, user_id)
        if not user:
            return False
        await session.delete(user)
        await session.commit()
        return True
