from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class AuthSchema(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
