from sqlalchemy.ext.asyncio import AsyncSession

from src.core.permissions import PermissionEnum
from src.permissions.models import PermissionRoleAssociation
from src.account.repositories.role import RoleRepository
from src.permissions.models import Permissions
from src.permissions.repositories import PermissionRepository


async def init_permissions(session: AsyncSession):
    permission_repository = PermissionRepository(session=session)
    role_repository = RoleRepository(session=session)
    permissions_in_db = await permission_repository.get_all_permissions()

    permissions_in_db_names = {permission.name for permission in permissions_in_db}
    actual_permissions = {permission.value for permission in PermissionEnum}

    new_permission_names = actual_permissions - permissions_in_db_names

    for name in new_permission_names:
        session.add(Permissions(name=name))

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

    for name in actual_permissions:
        if name not in current_admin_permission_names:
            association = PermissionRoleAssociation(
                role_id=admin_role.id, permission_id=name_to_permission[name].id
            )
            session.add(association)

    for association in list(admin_role.permission_associations or []):
        if association.permission.name not in actual_permissions:
            await session.delete(association)

    await session.commit()
