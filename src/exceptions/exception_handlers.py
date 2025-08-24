from abc import ABC, abstractmethod
from builtins import Exception
from cgitb import handler
from typing import Optional

from fastapi import Request, HTTPException, status, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.exceptions.schemas.exceptions import (
    ErrorDetail,
    ExceptionTypeEnum,
    ErrorResponseSchema,
)
from src.exceptions.exceptions import BaseCustomException


class ExceptionHandler(ABC):
    """Абстрактный класс для обработки исключений"""

    @staticmethod
    def create_error_detail(
        message: str, details: str | None = None, value: str | None = None
    ) -> ErrorDetail:
        return ErrorDetail(message=message, details=details, value=value)

    @staticmethod
    def create_error_response(
        exception_type: ExceptionTypeEnum,
        status_code: int,
        description: list[ErrorDetail],
    ) -> ErrorResponseSchema:
        return ErrorResponseSchema(
            exception_type=exception_type,
            status_code=status_code,
            description=description,
        )

    @abstractmethod
    async def handle(self, request: Request, exc: Exception) -> JSONResponse:
        pass


class CustomExceptionHandler(ExceptionHandler):
    """Обработка кастомных исключений"""

    async def handle(self, request: Request, exc: BaseCustomException) -> JSONResponse:
        error_response = self.create_error_response(
            exception_type=exc.exception_type,
            status_code=exc.status_code,
            description=exc.errors,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump(),
        )


class HTTPExceptionHandler(ExceptionHandler):
    """Обработка стандартных HTTPException"""

    async def handle(self, request: Request, exc: HTTPException) -> JSONResponse:
        error_detail = self.create_error_detail(
            message=exc.detail, details="Standard HTTP error occurred", value=None
        )

        error_response = self.create_error_response(
            exception_type=ExceptionTypeEnum.USER,
            status_code=exc.status_code,
            description=[error_detail],
        )
        return JSONResponse(
            status_code=exc.status_code, content=error_response.model_dump()
        )


class ValidationExceptionHandler(ExceptionHandler):
    """Обработчик ошибок валидации FastAPI"""

    async def create_list_errors(self, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            field = ".".join(
                str(loc) for loc in error["loc"] if loc not in ["body", "query", "path"]
            )
            errors.append(
                self.create_error_detail(
                    message=error["msg"],
                    details=f"Field: {field}, Type: {error['type']}",
                    value=str(error.get("input", "None")),
                )
            )
        return errors

    async def handle(
        self, request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = await self.create_list_errors(exc=exc)
        error_response = self.create_error_response(
            exception_type=ExceptionTypeEnum.VALIDATION,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            description=errors,
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response.model_dump(),
        )


class GeneralExceptionHandler(ExceptionHandler):
    """Обрабатывает все необработанные исключения"""

    async def handle(self, request: Request, exc: Exception) -> JSONResponse:
        error_detail = self.create_error_detail(
            message="Iternal server error", details=str(exc), value=None
        )

        error_response = self.create_error_response(
            exception_type=ExceptionTypeEnum.SERVER,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            description=[error_detail],
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(),
        )


class ExceptionHandlerFactory:
    """Фабрика для управления обработчиками исключений"""

    def __init__(self):
        self.handlers: dict[type[Exception], ExceptionHandler]
        self._initialize_handlers()

    def _initialize_handlers(self):
        """Инициализация обработчиков"""
        self.handlers = {
            BaseCustomException: CustomExceptionHandler(),
            HTTPException: HTTPExceptionHandler(),
            RequestValidationError: ValidationExceptionHandler(),
            Exception: GeneralExceptionHandler(),
        }

    def get_handler(
        self, exception_type: type[Exception]
    ) -> Optional[ExceptionHandler]:
        """Возврат обработчика под тип исключения"""
        for handler_type, handler in self.handlers.items():
            if issubclass(exception_type, handler_type):
                return handler
        return None

    async def handle_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """Обрабатывает исключение с помощью подходящего обработчика"""
        handler = self.get_handler(type(exc))
        if handler:
            return await handler.handle(request=request, exc=exc)

        general_handler = GeneralExceptionHandler()
        return await general_handler.handle(request=request, exc=exc)


class ExceptionHandlerManager:
    def __init__(self, app):
        self.app: FastAPI = app
        self.factory = ExceptionHandlerFactory()

    def register_handlers(self):
        @self.app.exception_handler(BaseCustomException)
        async def custom_exception_handler(request: Request, exc: BaseCustomException):
            handler = self.factory.get_handler(exception_type=type(exc))
            return await handler.handle(request=request, exc=exc)

        @self.app.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc: HTTPException):
            handler = self.factory.get_handler(exception_type=HTTPException)
            return await handler.handle(request=request, exc=exc)

        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(
            request: Request, exc: RequestValidationError
        ):
            handler = self.factory.get_handler(exception_type=RequestValidationError)
            return await handler.handle(request=request, exc=exc)

        @self.app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception):
            handler = self.factory.get_handler(
                exception_type=type(exc)
            ) or self.factory.get_handler(Exception)
            return await handler.handle(request=request, exc=exc)

    @classmethod
    def setup(cls, app):
        manager = cls(app)
        manager.register_handlers()
        return manager
