from fastapi import APIRouter
from src.account.routers import router as account_router
from src.authentication.routers import router as auth_router


router = APIRouter(prefix="/api/v1")
router.include_router(account_router)
router.include_router(auth_router)
