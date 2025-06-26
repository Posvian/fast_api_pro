import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime | None = None

    @field_validator("password")
    def validate_password(cls, value) -> str:
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
        if not re.match(pattern, value):
            raise ValueError(
                "Пароль должен быть больше 8 символов и содержать хотя бы 1 заглавную букву, строчную букву, спецсимвол и цифру."
            )
        return value


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime | None = None
    # is_superuser: bool
    # is_active: bool


class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: datetime


class UserPartialUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime | None = None
