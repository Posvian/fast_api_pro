from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.servicies import UserService
from src.core.orm.db import get_async_session


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
):
    return UserService(session=session)
