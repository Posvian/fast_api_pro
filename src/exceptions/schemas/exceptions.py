from enum import Enum
from pydantic import BaseModel


class ExceptionTypeEnum(str, Enum):
    USER = "USER"
    SERVER = "SERVER"
    VALIDATION = "VALIDATION"


class ErrorDetail(BaseModel):
    message: str
    details: str | None = None
    value: str | None = None


class ErrorResponseSchema(BaseModel):
    exception_type: ExceptionTypeEnum
    status_code: int
    description: list[ErrorDetail]
