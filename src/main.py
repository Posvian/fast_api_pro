from typing import Union

from fastapi import FastAPI, APIRouter
from core.router import router

app = FastAPI(
    docs_url='/api/docs',
    openapi_url='/api/openapi.json'
)

app.include_router(router)


