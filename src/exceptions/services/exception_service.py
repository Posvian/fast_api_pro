from fastapi import status

from src.exceptions.exceptions import BaseCustomException
from src.exceptions.schemas.exceptions import ExceptionTypeEnum
from src.exceptions.schemas.exceptions import ErrorDetail
from src.exceptions.exceptions import (
    UserException,
    ValidationException,
    ServerException,
    NotFoundException,
)


class ExceptionService:
    """Сервис для создания и выброса исключений"""

    @staticmethod
    def create_error(
        message: str, details: str | None = None, value: str | None = None
    ) -> ErrorDetail:
        return ErrorDetail(message=message, details=details, value=value)

    @classmethod
    def raise_error(
        cls,
        exception_class: type[BaseCustomException],
        exception_type: ExceptionTypeEnum,
        status_code: int,
        message: str,
        details: str | None = None,
        value: str | None = None,
    ):
        error = cls.create_error(message=message, details=details, value=value)
        raise exception_class(
            exception_type=exception_type, status_code=status_code, errors=[error]
        )

    @classmethod
    def user_error(
        cls, message: str, details: str | None = None, value: str | None = None
    ):
        error = cls.create_error(message=message, details=details, value=value)
        raise UserException(errors=[error])

    @classmethod
    def validation_error(
        cls, message: str, details: str | None, value: str | None = None
    ):
        error = cls.create_error(message=message, details=details, value=value)
        raise ValidationException(errors=[error])

    @classmethod
    def not_found_error(
        cls, message: str, details: str | None = None, value: str | None = None
    ):
        error = cls.create_error(message=message, details=details, value=value)
        raise NotFoundException(errors=[error])

    @classmethod
    def server_error(
        cls, message: str, details: str | None = None, value: str | None = None
    ):
        error = cls.create_error(message=message, details=details, value=value)
        raise ServerException(errors=[error])

    @classmethod
    def field_validation_error(
        cls,
        field_name: str,
        message: str,
        value: str | None = None,
        expected_type: str | None = None,
    ):
        details = f"Field: {field_name}"
        if expected_type:
            details += f", Expected type: {expected_type}"
        cls.validation_error(message=message, details=details, value=value)
