import re
from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

from .role import RoleResponseSchema


NAME_SURNAME_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class BaseUserSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

    @field_validator("first_name")
    def validate_first_name(cls, value) -> str:
        if not NAME_SURNAME_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Имя должно состоять только из букв"
            )
        return value

    @field_validator("last_name")
    def validate_last_name(cls, value) -> str:
        if not NAME_SURNAME_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Фамилия должна состоять только из букв"
            )
        return value


class UserCreateSchema(BaseUserSchema):
    password: str
    role_id: int | None = None

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
    role: RoleResponseSchema | None = None


class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    role_id: int


class UserPartialUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    role_id: int | None = None
