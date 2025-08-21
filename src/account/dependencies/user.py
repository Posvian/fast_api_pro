from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.servicies import UserService
from src.core.orm.db import get_async_session


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
):
    return UserService(session=session)


async def get_user_filters(
    first_name: str | None = None,
    last_name: str | None = None,
    email__eq: str | None = None,
) -> dict:
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email__eq,
    }
