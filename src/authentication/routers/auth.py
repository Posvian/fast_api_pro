from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from src.authentication.dependencies.auth import get_auth_service
from src.authentication.services.auth import AuthenticationService
from src.core.constants import credentials_exception
from src.authentication.schemas.auth import AuthSchema, Token, User
from src.account.dependencies.user import get_user_service
from src.account.servicies import UserService
from src.account.schemas import UserResponseSchema

from src.authentication.dependencies.auth import get_current_active_user

router = APIRouter(prefix="/jwt", tags=["AUTHENTICATION"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/authentication/jwt/token")


@router.get("/me", response_model=User)
async def get_me_handler(
    current_user: UserResponseSchema = Depends(get_current_active_user),
):
    return current_user


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> Token:
    user = await auth_service.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise credentials_exception
    data = AuthSchema(email=form_data.username, password=form_data.password)
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
