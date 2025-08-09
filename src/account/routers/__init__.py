from fastapi import APIRouter
from src.account.routers.users import router as user_router

from src.account.routers.roles import router as role_router

router = APIRouter(prefix="/account")
router.include_router(user_router)
router.include_router(role_router)
