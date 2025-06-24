from fastapi import APIRouter
from .users import router as user_router

router = APIRouter(prefix="/account", tags=["ACCOUNT"])
router.include_router(user_router)