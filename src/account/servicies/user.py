from datetime import datetime
from typing import Sequence

from dns.rdata import Rdata
from fastapi import HTTPException, status

from fastapi.exceptions import ValidationException
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.repositories.user import UserRepository
from src.account.schemas import (
    UserCreateSchema,
    UserUpdateSchema,
    UserPartialUpdateSchema,
    UserResponseSchema,
    RoleResponseSchema,
)
from src.account.models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session=session)

    async def get_all(self, offset: int, per_page: int) -> Sequence[User]:
        return await self.repository.get_all(offset=offset, per_page=per_page)

    async def check_exist(self, email):
        if await self.repository.get_by_email(email=email):
            raise HTTPException(
                detail="Пользователь с таким майлом уже существует",
                status_code=status.HTTP_409_CONFLICT,
            )

    async def create(self, user_schema: UserCreateSchema):
        await self.check_exist(email=user_schema.email)
        user = await self.repository.create(user_schema=user_schema)
        return user

    async def get_by_id(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                detail="Такого пользователя не существует",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return user

    async def update_user(self, user_id: int, user_schema: UserUpdateSchema):
        user = await self.get_by_id(user_id=user_id)
        return await self.repository.update(user=user, user_schema=user_schema)

    async def partial_update_user(
        self, user_id: int, user_schema: UserPartialUpdateSchema
    ):
        user = await self.get_by_id(user_id=user_id)
        return await self.repository.partial_update(user=user, user_schema=user_schema)

    async def delete(self, user_id: int):
        user = await self.get_by_id(user_id=user_id)
        await self.repository.delete(user=user)
