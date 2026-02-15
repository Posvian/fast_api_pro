from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.core.orm.db import async_session_maker
from src.core.router import router
from src.core.init_admin import init_admin_user
from src.core.init_permissions import init_permissions
from src.exceptions.exception_handlers import ExceptionHandlerManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_maker() as session:
        await init_admin_user(session=session)
        await init_permissions(session=session)

    yield


app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json", lifespan=lifespan)


app.include_router(router)


handler_manager = ExceptionHandlerManager.setup(app=app)
