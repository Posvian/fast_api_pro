import pytest_asyncio

from src.account.schemas import RoleCreateSchema
from src.account.servicies.role import RoleService


@pytest_asyncio.fixture
async def get_role_payload():
    test_name = "test_admin"
    return {"name": test_name}


@pytest_asyncio.fixture
async def create_test_role(async_session, get_role_payload):
    role_service = RoleService(async_session)
    role_schema = RoleCreateSchema(**get_role_payload)
    return await role_service.create(role_schema=role_schema)


@pytest_asyncio.fixture
async def get_role_from_database(async_session):
    async def _get_role_from_database_by_id(role_id: int):
        role_service = RoleService(async_session)
        return await role_service.get_by_id(role_id=role_id)

    return _get_role_from_database_by_id
