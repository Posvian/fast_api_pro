from fastapi import APIRouter


from src.authentication.routers.auth import router as auth_router


router = APIRouter(prefix="/authentication")
router.include_router(auth_router)
