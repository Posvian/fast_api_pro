from src.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from typing import AsyncGenerator


ASYNC_DATABASE_URL = f"postgresql+asyncpg://{settings.db.db_user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}"
SYNC_DATABASE_URL = f"postgresql+psycopg2://{settings.db.db_user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}"

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
sync_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


def get_sync_session():
    with Session(sync_engine) as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
