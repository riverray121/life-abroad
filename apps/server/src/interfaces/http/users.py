from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel
from src.domain.models.user import User
from src.domain.services.user_service import UserService
from src.infrastructure.database import get_session
from src.domain.errors.custom_errors import UserNotFoundError
from typing import Sequence

router = APIRouter(prefix="/users", tags=["users"])

# Create request models
class UserCreateRequest(BaseModel):
    name: str
    phone_number: str
    email: str | None = None

class UserUpdateRequest(BaseModel):
    name: str | None = None
    phone_number: str | None = None
    email: str | None = None

user_service = UserService()

@router.get("/", response_model=Sequence[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    return await user_service.list_users(session)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateRequest, session: AsyncSession = Depends(get_session)):
    return await user_service.create_user(user.name, user.phone_number, user.email, session)

@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdateRequest, session: AsyncSession = Depends(get_session)):
    try:
        return await user_service.update_user(user_id, session, user.name, user.phone_number, user.email)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        await user_service.delete_user(user_id, session)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
