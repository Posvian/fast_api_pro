import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class BaseUserSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserCreateSchema(BaseUserSchema):
    password: str

    @field_validator("password")
    def validate_password(cls, value) -> str:
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
        if not re.match(pattern, value):
            raise ValueError(
                "Пароль должен быть больше 8 символов и содержать хотя бы 1 заглавную букву, строчную букву, спецсимвол и цифру."
            )

        return value


class UserResponseSchema(BaseUserSchema):
    id: int
    is_superuser: bool | None = None
    is_active: bool | None = None


class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str


class UserPartialUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
