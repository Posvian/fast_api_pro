from sqlalchemy.ext.asyncio import AsyncSession

from src.permissions.repositories import PermissionRepository


class PermissionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = PermissionRepository(session=session)

    async def get_user_permissions(self, user_id: int) -> list[str]:
        return await self.repository.get_user_permissions(user_id=user_id)
