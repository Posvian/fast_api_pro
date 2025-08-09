from typing import Sequence

from dns.e164 import query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from account.models import Role
from account.schemas import RoleCreateSchema


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, offset: int, per_page: int) -> Sequence[Role]:
        query = select(Role).offset(offset).limit(per_page)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_name(self, name: str) -> Role | None:
        query = select(Role).where(Role.name == name)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_by_id(self, role_id: int) -> Role | None:
        query = select(Role).where(Role.id == role_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def create(self, role_schema: RoleCreateSchema) -> Role:
        role = Role(
            name=role_schema.name,
        )
        self.session.add(role)
        await self.session.commit()
        await self.session.flush()

        return role

    async def delete(self, role: Role):
        await self.session.delete(role)
        await self.session.commit()
