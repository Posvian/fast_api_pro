from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.schemas import UserResponseSchema
from src.authentication.services.auth import AuthenticationService
from src.core.orm.db import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_auth_service(session: AsyncSession = Depends(get_async_session)):
    return AuthenticationService(session=session)
