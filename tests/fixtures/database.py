import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.core.orm import Base


class TestDatabase:
    def __init__(self):
        self.database_url = f"postgresql+asyncpg://{settings.db.test_db_user}:{settings.db.test_db_password}@{settings.db.test_host}:{settings.db.test_port}/{settings.db.test_name}"
        self.engine = create_async_engine(self.database_url)
        self.session_maker = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_database(self):
        try:
            conn = await asyncpg.connect(
                host=settings.db.test_host,
                port=settings.db.test_port,
                user=settings.db.test_db_user,
                password=settings.db.test_db_password,
                database=settings.db.test_name,
            )
            await conn.close()

        except asyncpg.InvalidCatalogNameError:
            sys_conn = await asyncpg.connect(
                host=settings.db.test_host,
                port=settings.db.test_port,
                user=settings.db.test_db_user,
                password=settings.db.test_db_password,
            )
            try:
                await sys_conn.execute(
                    f'CREATE DATABASE "{settings.db.test_name}" OWNER "{settings.db.test_db_user}"'
                )
            finally:
                await sys_conn.close()

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        await self.engine.dispose()
