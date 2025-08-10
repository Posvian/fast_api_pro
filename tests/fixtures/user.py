import pytest
import pytest_asyncio
from sqlalchemy import select

from src.account.models import Role
from src.account.schemas import UserCreateSchema
from src.account.servicies import UserService
from tests.conftest import async_session
from tests.constants import SELECT_USER_BY_ID


@pytest_asyncio.fixture
async def get_user_payload():
    test_email = "test@test.ru"
    test_first_name = "Test"
    test_last_name = "Ivanov"
    test_password = "Av!12345"
    return {
        "email": test_email,
        "first_name": test_first_name,
        "last_name": test_last_name,
        "password": test_password,
    }


@pytest_asyncio.fixture
async def get_update_user_payload():
    test_update_first_name = "Test_update"
    test_update_last_name = "Updated"
    test_update_role_id = 1
    return {
        "first_name": test_update_first_name,
        "last_name": test_update_last_name,
        "role_id": test_update_role_id,
    }


@pytest_asyncio.fixture
async def create_test_user(async_session, get_user_payload, create_test_role):
    user_service = UserService(async_session)
    user_schema = UserCreateSchema(**get_user_payload)
    return await user_service.create(user_schema=user_schema)


@pytest_asyncio.fixture
async def get_user_from_database(async_session):
    async def _get_user_from_database_by_id(user_id: int):
        user_service = UserService(async_session)
        return await user_service.get_by_id(user_id=user_id)

    return _get_user_from_database_by_id
