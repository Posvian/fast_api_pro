from fastapi import HTTPException, status
from src.exceptions.schemas.exceptions import ErrorDetail, ExceptionTypeEnum


class BaseCustomException(Exception):
    """Базовое кастомное исключение"""

    def __init__(
        self,
        exception_type: ExceptionTypeEnum,
        status_code: int,
        errors: list[ErrorDetail],
    ):
        self.exception_type = exception_type
        self.status_code = status_code
        self.errors = errors
        super().__init__(
            f"{exception_type} error: {[error.message for error in errors]}"
        )


class UserException(BaseCustomException):
    """Пользовательские ошибки (400-499)"""

    def __init__(self, errors: list[ErrorDetail]):
        super().__init__(
            exception_type=ExceptionTypeEnum.USER,
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=errors,
        )


class ServerException(BaseCustomException):
    """Ошибки сервера (500)"""

    def __init__(self, errors: list[ErrorDetail]):
        super().__init__(
            exception_type=ExceptionTypeEnum.SERVER,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            errors=errors,
        )


class ValidationException(BaseCustomException):
    """Ошибки валидации (422)"""

    def __init__(self, errors: list[ErrorDetail]):
        super().__init__(
            exception_type=ExceptionTypeEnum.VALIDATION,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            errors=errors,
        )


class NotFoundException(BaseCustomException):
    """Ошибка NotFoundError (404)"""

    def __init__(self, errors: list[ErrorDetail]):
        super().__init__(
            exception_type=ExceptionTypeEnum.USER,
            status_code=status.HTTP_404_NOT_FOUND,
            errors=errors,
        )
