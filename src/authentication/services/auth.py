from datetime import datetime, timezone, timedelta

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.schemas.auth import AuthSchema
from src.account.models.user import User
from src.account.repositories.user import UserRepository
from src.core.config import settings
from src.core.constants import credentials_exception


class AuthenticationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session=session)
        self.pwd_context = CryptContext(
            schemes=[settings.auth.scheme], deprecated="auto"
        )

    async def create_jwt_token(
        self, data: AuthSchema, expires_delta: timedelta, token_type: str | None = None
    ):
        payload = {
            "email": data.email,
            "type": token_type,
            "exp": datetime.now(timezone.utc) + expires_delta,
        }
        return jwt.encode(
            payload=payload,
            key=settings.auth.secret_key,
            algorithm=settings.auth.algorithm,
        )

    async def encode_access_token(self, data: AuthSchema):
        return await self.create_jwt_token(
            data=data,
            expires_delta=timedelta(minutes=settings.auth.expire_time),
            token_type="access",
        )

    async def encode_refresh_token(self, data: AuthSchema):
        return await self.create_jwt_token(
            data=data,
            expires_delta=timedelta(days=settings.auth.refresh_token_expire),
            token_type="refresh",
        )

    async def token_data(self, data: AuthSchema):
        access_token = await self.encode_access_token(data=data)
        refresh_token = await self.encode_refresh_token(data=data)
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def decode_jwt(self, token: str, refresh: bool = False):
        try:
            payload = jwt.decode(
                token,
                key=settings.auth.secret_key,
                algorithms=[settings.auth.algorithm],
                options={"verify_exp": False},
            )
        except jwt.ExpiredSignatureError:
            raise InvalidTokenError("Token expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Invalid token")

        exp = payload.get("exp")
        if exp is None:
            raise InvalidTokenError("Missing exp claim")
        await self.check_token_expire(exp=exp)

        expected_type = "refresh" if refresh else "access"
        if payload.get("type") != expected_type:
            raise InvalidTokenError(f"Wrong token type, expected {expected_type}")

        return payload

    async def decode_refresh_jwt(self, token):
        return await self.decode_jwt(token, refresh=True)

    @staticmethod
    async def check_token_expire(exp):
        if datetime.fromtimestamp(float(exp)) - datetime.now() < timedelta(0):
            raise credentials_exception

    async def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def verify_password(self, plain_password, user_password):
        return self.pwd_context.verify(plain_password, user_password)

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.user_repository.get_by_email(email=email)
        if not user:
            raise credentials_exception
        if not await self.verify_password(
            plain_password=password, user_password=user.password
        ):
            raise credentials_exception
        return user
