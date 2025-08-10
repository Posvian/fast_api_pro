from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.servicies.role import RoleService
from src.core.orm.db import get_async_session


async def get_role_service(session: AsyncSession = Depends(get_async_session)):
    return RoleService(session=session)
