import pytest
import pytest_asyncio
import asyncio
import asyncpg

from sqlalchemy.ext.asyncio import AsyncSession
from tests.fixtures.database import TestDatabase

from src.core.permissions import PermissionEnum
from src.account.models import Role, User
from src.permissions.models import Permissions, PermissionRoleAssociation
from src.authentication.services.auth import AuthenticationService

pytest_plugins = [
    "tests.fixtures.client",
    "tests.fixtures.async_session",
    "tests.fixtures.user",
    "tests.fixtures.role",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_db():
    db = TestDatabase()
    await db.create_database()
    yield db
    await db.close()


@pytest_asyncio.fixture
async def create_tables(test_db):
    await test_db.create_tables()
    yield


@pytest_asyncio.fixture
async def async_session(test_db) -> AsyncSession:
    async with test_db.session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="session")
async def asyncpg_pool():
    db = TestDatabase()
    pool = await asyncpg.create_pool("".join(db.database_url.split("+asyncpg")))
    yield pool
    pool.close()


@pytest_asyncio.fixture
async def auth_headers_with_all_permissions(async_client, async_session):
    role = Role(name="test_role")
    app_permissions = [
        Permissions(name=permission.value) for permission in PermissionEnum
    ]
    associations = [
        PermissionRoleAssociation(role=role, permission=permission)
        for permission in app_permissions
    ]
    async_session.add_all([role, *app_permissions, *associations])
    await async_session.commit()

    auth_service = AuthenticationService(async_session)
    hashed_password = await auth_service.get_password_hash("test_password")
    user = User(email="test@test.ru", password=hashed_password, role=role)
    async_session.add(user)
    await async_session.commit()

    response = await async_client.post(
        "/api/v1/authentication/jwt/token",
        json={"email": "test@test.ru", "password": "test_password"},
    )

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
