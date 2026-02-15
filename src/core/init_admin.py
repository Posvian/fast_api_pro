from sqlalchemy.ext.asyncio import AsyncSession

from src.account.schemas import RoleCreateSchema
from src.account.repositories.user import UserRepository
from src.account.repositories.role import RoleRepository
from src.account.models.user import User
from src.account.models.role import Role
from src.authentication.services.auth import AuthenticationService

from src.core.config import settings


async def init_admin_user(session: AsyncSession) -> None:
    auth_service = AuthenticationService(session=session)
    role_repository = RoleRepository(session=session)
    user_repository = UserRepository(session=session)

    admin_role = await role_repository.get_by_name("admin")
    if admin_role is None:
        role_schema = RoleCreateSchema(name="admin")
        admin_role = await role_repository.create(role_schema=role_schema)

    superuser = await user_repository.get_superuser()
    if superuser is None:
        password = await auth_service.get_password_hash(settings.admin.password)
        superuser = User(
            email=settings.admin.email,
            password=password,
            first_name=settings.admin.first_name,
            last_name=settings.admin.last_name,
            is_superuser=True,
            is_active=True,
            role_id=admin_role.id,
        )
        session.add(superuser)
        await session.commit()
    elif superuser.role_id != admin_role.id:
        superuser.role_id = admin_role.id
        await session.commit()
