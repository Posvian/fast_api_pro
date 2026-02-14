from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.permissions.models.permissions import Permissions, PermissionRoleAssociation
from src.account.models import User, Role


class PermissionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_permissions(self):
        query = select(Permissions)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_user_permissions(self, user_id: int) -> list[str]:
        query = (
            select(Permissions.name)
            .join(
                PermissionRoleAssociation,
                PermissionRoleAssociation.permission_id == Permissions.id,
            )
            .join(Role, Role.id == PermissionRoleAssociation.role_id)
            .join(User, User.role_id == Role.id)
            .where(User.id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
