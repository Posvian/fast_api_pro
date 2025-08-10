from fastapi import APIRouter
from src.account.routers import router as account_router


router = APIRouter(prefix="/api/v1")
router.include_router(account_router)
