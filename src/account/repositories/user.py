from typing import Sequence

from dns.e164 import query
from fastapi import HTTPException

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.account.schemas import (
    UserCreateSchema,
    UserUpdateSchema,
    UserPartialUpdateSchema,
)
from src.account.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def count_users(self):
        query = select(func.count()).select_from(User)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all(self, offset: int, per_page: int) -> Sequence[User]:
        query = (
            select(User)
            .options(joinedload(User.role))
            .offset(offset)
            .limit(per_page)
            .order_by(User.id)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_email(self, email) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_by_id(self, user_id) -> User | None:
        query = select(User).options(joinedload(User.role)).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def create(self, user_schema: UserCreateSchema) -> User:
        user = User(
            email=user_schema.email,
            first_name=user_schema.first_name,
            last_name=user_schema.last_name,
            password=user_schema.password,
            role_id=user_schema.role_id,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.flush()
        await self.session.refresh(user)
        return await self.get_by_id(user_id=user.id)

    async def update(self, user: User, user_schema: UserUpdateSchema) -> User:
        user.first_name = user_schema.first_name
        user.last_name = user_schema.last_name
        user.role_id = user_schema.role_id
        await self.session.commit()
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def partial_update(
        self, user: User, user_schema: UserPartialUpdateSchema
    ) -> User:
        for name, value in user_schema.model_dump().items():
            if value is not None:
                setattr(user, name, value)
        await self.session.commit()
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
