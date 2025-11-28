from sqlalchemy.ext.asyncio import AsyncSession

from src.permissions.models import PermissionRoleAssociation
from src.account.repositories.role import RoleRepository
from src.permissions.models import Permissions
from src.permissions.repositories import PermissionRepository

ALL_PERMISSIONS = [
    "user:create",
    "user:read",
    "user:update",
    "user:delete",
    "role:read",
    "role:update",
    "role:delete",
]


async def init_permissions(session: AsyncSession):
    permission_repository = PermissionRepository(session=session)
    role_repository = RoleRepository(session=session)
    permissions_in_db = await permission_repository.get_all_permissions()

    permissions_in_db_names = {permission.name for permission in permissions_in_db}

    new_permission_names = set(ALL_PERMISSIONS) - permissions_in_db_names
    extra_permission_names = permissions_in_db_names - set(ALL_PERMISSIONS)

    for name in new_permission_names:
        session.add(Permissions(name=name))

    for permission in permissions_in_db:
        if permission.name in extra_permission_names:
            await session.delete(permission)

    await session.commit()

    admin_role = await role_repository.get_by_name_with_permissions(name="admin")
    if not admin_role:
        return

    updated_permissions = await permission_repository.get_all_permissions()
    name_to_permission = {
        permission.name: permission for permission in updated_permissions
    }

    current_admin_permission_names = {
        association.permission.name
        for association in admin_role.permission_associations or []
    }

    for name in ALL_PERMISSIONS:
        if name not in current_admin_permission_names:
            association = PermissionRoleAssociation(
                role_id=admin_role.id, permission_id=name_to_permission[name].id
            )
            session.add(association)

    for association in list(admin_role.permission_associations or []):
        if association.permission.name not in ALL_PERMISSIONS:
            await session.delete(association)

    await session.commit()
