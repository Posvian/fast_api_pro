from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.permissions.dependencies.permission import get_permission_service
from src.permissions.servicies import PermissionService
from src.account.dependencies.user import get_user_service
from src.account.servicies import UserService
from src.account.models.user import User
from src.authentication.services.auth import AuthenticationService
from src.core.orm.db import get_async_session
from src.core.constants import credentials_exception

bearer_scheme = HTTPBearer()


async def get_auth_service(session: AsyncSession = Depends(get_async_session)):
    return AuthenticationService(session=session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthenticationService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
) -> User:

    token = credentials.credentials
    try:
        payload = await auth_service.decode_jwt(token=token)
        email = payload.get("email")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await user_service.get_by_email(email=email)
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def require_permission(permission_name: str):
    async def _require_permission(
        current_user: User = Depends(get_current_user),
        permission_service: PermissionService = Depends(get_permission_service),
    ):
        if current_user.is_superuser:
            return

        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )

        permissions = await permission_service.get_user_permissions(current_user.id)

        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You`re lack required permission {permission_name}",
            )

    return _require_permission
