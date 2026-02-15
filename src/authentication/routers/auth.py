from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from src.authentication.dependencies.auth import get_auth_service
from src.authentication.services.auth import AuthenticationService
from src.core.constants import credentials_exception
from src.authentication.schemas.auth import AuthSchema, Token, User, RefreshTokenRequest
from src.account.dependencies.user import get_user_service
from src.account.servicies import UserService
from src.account.schemas import UserResponseSchema

from src.authentication.dependencies.auth import get_current_active_user

router = APIRouter(prefix="/jwt", tags=["AUTHENTICATION"])

bearer_scheme = HTTPBearer()


@router.get("/me", response_model=User)
async def get_me_handler(
    current_user: UserResponseSchema = Depends(get_current_active_user),
):
    return current_user


@router.post("/token")
async def login(
    data: AuthSchema,
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> Token:
    user = await auth_service.authenticate_user(
        email=data.email, password=data.password
    )
    if not user:
        raise credentials_exception
    data = AuthSchema(email=data.email, password=data.password)
    token_data = await auth_service.token_data(data=data)
    return Token(
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
    )


@router.post("/register")
async def register_user_handler(
    data: AuthSchema,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> Token:
    token_data = await auth_service.token_data(data=data)
    await user_service.create(user_schema=data)
    return Token(
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
    )


@router.get("/verification")
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthenticationService = Depends(get_auth_service),
):
    token = credentials.credentials
    try:
        payload = await auth_service.decode_jwt(token=token)
        return {"valid": True, "email": payload.get("email")}
    except InvalidTokenError:
        return {"valid": False}


@router.post("/refresh")
async def refresh_token(
    data: RefreshTokenRequest,
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> Token:

    payload = await auth_service.decode_refresh_jwt(data.refresh_token)
    email = payload.get("email")
    if not email:
        raise InvalidTokenError("Invalid refresh token payload")
    token_data = await auth_service.token_data(
        data=AuthSchema(email=email, password=None)
    )
    return Token(
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
    )
