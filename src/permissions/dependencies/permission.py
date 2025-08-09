from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.orm.db import get_async_session
from permissions.servicies import PermissionService


def get_permission_service(session: AsyncSession = Depends(get_async_session)):
    return PermissionService(session=session)
