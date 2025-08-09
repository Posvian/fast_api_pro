from sqlalchemy.ext.asyncio import AsyncSession

from permissions.repositories import PermissionRepository


class PermissionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = PermissionRepository(session=session)
