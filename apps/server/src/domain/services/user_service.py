from typing import Sequence
from sqlmodel.ext.asyncio.session import AsyncSession
from src.domain.models.user import User
from src.infrastructure.repositories.user_repository import UserRepository
from src.domain.errors.custom_errors import UserNotFoundError

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def create_user(self, name: str, phone_number: str, email: str | None, session: AsyncSession) -> User:
        user = User(name=name, phone_number=phone_number, email=email)
        return await self.user_repository.create_user(user, session)

    async def list_users(self, session: AsyncSession) -> Sequence[User]:
        return await self.user_repository.get_all_users(session)

    async def get_user_by_id(self, user_id: int, session: AsyncSession) -> User | None:
        return await self.user_repository.get_user_by_id(user_id, session)

    async def update_user(self, user_id: int, session: AsyncSession, name: str | None = None, phone_number: str | None = None, email: str | None = None) -> User:
        user = await self.user_repository.get_user_by_id(user_id, session)
        if not user:
            raise UserNotFoundError(user_id)
        
        if name is not None:
            user.name = name
        if phone_number is not None:
            user.phone_number = phone_number
        if email is not None:
            user.email = email
            
        return await self.user_repository.update_user(user, session)

    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        deleted = await self.user_repository.delete_user(user_id, session)
        if not deleted:
            raise UserNotFoundError(user_id)
