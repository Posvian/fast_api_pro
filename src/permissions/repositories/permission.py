from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.permissions.models.permissions import Permissions


class PermissionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_permissions(self):
        query = select(Permissions)
        result = await self.session.execute(query)
        return result.scalars().all()
