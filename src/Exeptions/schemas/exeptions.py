from enum import Enum
from pydantic import BaseModel


class ExceptionType(str, Enum):
    USER = "USER"
    SERVER = "SERVER"
    VALIDATION = "VALIDATION"


class ErrorDetail(BaseModel):
    message: str
    details: str | None = None
    value: str | None = None


class ErrorSchema(BaseModel):
    exception_tipe: ExceptionType
    status_code: int
    description: list[ErrorDetail]
