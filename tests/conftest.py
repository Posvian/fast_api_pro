import pytest
import pytest_asyncio
import asyncio
import asyncpg

from sqlalchemy.ext.asyncio import AsyncSession

from tests.fixtures.database import TestDatabase

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


# @pytest.fixture
# async def get_user_from_database(asyncpg_pool):
#     async def get_user_from_database_by_id(user_id: int):
#         async with asyncpg_pool.acquire() as connection:
#             return await connection.fetch(SELECT_USER_BY_ID, user_id)
#
#     return get_user_from_database_by_id
