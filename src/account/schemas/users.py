from datetime import datetime

from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime | None = None


class UserResponseSchema(BaseModel):
    id: int
    email: str
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