import pytest_asyncio

from src.core.orm.db import get_async_session
from src.main import app


@pytest_asyncio.fixture(autouse=True)
async def override_async_session(async_session):
    app.dependency_overrides[get_async_session] = lambda: async_session
    yield
    app.dependency_overrides.pop(get_async_session, None)
