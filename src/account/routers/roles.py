from fastapi import APIRouter, status, Depends

from src.account.dependencies.role import get_role_service
from src.account.schemas import RoleCreateSchema, RoleListSchema
from src.account.servicies import RoleService

router = APIRouter(prefix="/roles", tags=["ACCOUNT/ROLES"], dependencies=[])


@router.get(
    "/",
    response_model=list[RoleListSchema],
    status_code=status.HTTP_200_OK,
    description="Получение списка ролей",
)
async def get_roles_handler(
    page: int, per_page: int = 10, role_service: RoleService = Depends(get_role_service)
):
    offset = (page - 1) * per_page
    return await role_service.get_all(offset=offset, per_page=per_page)


@router.get(
    "/{role_id}",
    response_model=RoleListSchema,
    status_code=status.HTTP_200_OK,
    description="Получение конкретной роли",
)
async def get_role_handler(
    role_id: int, role_service: RoleService = Depends(get_role_service)
):
    return await role_service.get_by_id(role_id=role_id)


@router.post(
    "/",
    response_model=RoleCreateSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание роли",
)
async def create_role_handler(
    payload: RoleCreateSchema,
    role_service: RoleService = Depends(get_role_service),
):
    return await role_service.create(role_schema=payload)


@router.delete(
    "/{role_id}", status_code=status.HTTP_204_NO_CONTENT, description="Удаление роли"
)
async def delete_role_handler(
    role_id: int, role_service: RoleService = Depends(get_role_service)
):
    return await role_service.delete(role_id=role_id)
