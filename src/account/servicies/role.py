from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.models import Role
from src.account.repositories.role import RoleRepository
from src.account.schemas import RoleCreateSchema, RoleListSchema, RoleResponseSchema


class RoleService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = RoleRepository(session=session)

    async def check_exist(self, name):
        if await self.repository.get_by_name(name=name):
            raise HTTPException(
                detail="Такая роль уже существует", status_code=status.HTTP_409_CONFLICT
            )

    async def get_all(
        self, offset: int, per_page: int, name__ilike: str
    ) -> RoleListSchema:
        count_of_roles = await self.repository.get_role_count()
        if count_of_roles % per_page == 0:
            count_of_pages = count_of_roles // per_page
        else:
            count_of_pages = count_of_roles // per_page + 1
        roles = [
            RoleResponseSchema(id=role.id, name=role.name)
            for role in await self.repository.get_all(
                offset=offset, per_page=per_page, name__ilike=name__ilike
            )
        ]
        return RoleListSchema(
            roles=roles,
            count_of_pages=count_of_pages,
            count_of_roles=count_of_roles,
        )
        #     {
        #     "roles": await self.repository.get_all(offset=offset, per_page=per_page),
        #     "count_of_pages": count_of_pages,
        #     "count_of_roles": count_of_roles,
        # }

    async def get_by_id(self, role_id: int) -> Role:
        role = await self.repository.get_by_id(role_id=role_id)
        if not role:
            raise HTTPException(
                detail="Такой роли не существует", status_code=status.HTTP_404_NOT_FOUND
            )
        return role

    async def create(self, role_schema: RoleCreateSchema):
        await self.check_exist(name=role_schema.name)
        return await self.repository.create(role_schema=role_schema)

    async def delete(self, role_id: int):
        role = await self.repository.get_by_id(role_id=role_id)
        await self.repository.delete(role=role)
