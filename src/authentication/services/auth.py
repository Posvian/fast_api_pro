from datetime import datetime, timezone, timedelta

import jwt
from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.provision import run_reap_dbs

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

    async def encode_token(self, data: AuthSchema):
        payload = {"email": data.email}
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.auth.expire_time
        )
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload=payload,
            key=settings.auth.secret_key,
            algorithm=settings.auth.algorithm,
        )
        return encoded_jwt

    async def decode_jwt(self, token: str):
        payload = jwt.decode(
            token, key=settings.auth.secret_key, algorithms=[settings.auth.algorithm]
        )
        return payload

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
