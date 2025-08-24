from typing import Union

from fastapi import FastAPI, APIRouter
from src.core.router import router
from src.exceptions.exception_handlers import ExceptionHandlerManager

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")


app.include_router(router)

handler_manager = ExceptionHandlerManager.setup(app=app)
