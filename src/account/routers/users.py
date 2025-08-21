from datetime import datetime
from typing import Union

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.exceptions import ValidationException, ResponseValidationError
from fastapi_filter import FilterDepends

from src.account.dependencies.user import get_user_service, get_user_filters
from src.account.schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
    UserPartialUpdateSchema,
    UserListSchema,
    UserFilter,
)
from src.account.servicies import UserService

router = APIRouter(prefix="/users", tags=["ACCOUNT/USERS"])


@router.get(
    "/",
    response_model=UserListSchema,
    status_code=status.HTTP_200_OK,
    description="Получение списка пользователей",
)
async def get_users_handler(
    page: int = 1,
    per_page: int = 10,
    user_service: UserService = Depends(get_user_service),
    filter_data: dict = Depends(get_user_filters),
) -> UserListSchema:
    offset = (page - 1) * per_page
    return await user_service.get_all(
        offset=offset, per_page=per_page, filter_data=filter_data
    )


@router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
    description="Получение пользователя",
)
async def get_user_by_id_handler(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_by_id(user_id=user_id)


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание пользователя",
)
async def create_user_handler(
    payload: UserCreateSchema, user_service: UserService = Depends(get_user_service)
) -> UserResponseSchema:
    return await user_service.create(user_schema=payload)


@router.put(
    "/{user_id}",
    response_model=UserResponseSchema,
    description="Обновление данных пользователя",
)
async def update_user_handler(
    user_id: int,
    payload: UserUpdateSchema,
    user_service: UserService = Depends(get_user_service),
) -> UserResponseSchema:
    return await user_service.update_user(user_id=user_id, user_schema=payload)


@router.patch(
    "/{user_id}",
    response_model=UserResponseSchema,
    description="Частичное обновление данных пользователя",
)
async def partial_update_user_handler(
    user_id: int,
    payload: UserPartialUpdateSchema,
    user_service: UserService = Depends(get_user_service),
) -> UserResponseSchema:
    return await user_service.partial_update_user(user_id=user_id, user_schema=payload)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление пользователя",
)
async def delete_user_handler(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    return await user_service.delete(user_id=user_id)


#
#
# @router.post("/", response_model=UserCreateSchema, description="Создание пользователя")
# def create_user_handler(payload: UserCreateSchema):
#     return payload
#
#
# @router.get(
#     "/",
#     response_model=list[UserResponseSchema],
#     description="Получение списка пользователей",
# )
# def get_users_handler():
#     user_service = UserService()
#     return user_service.get_user_list()
#
#
# @router.put(
#     "/{user_id}",
#     response_model=UserUpdateSchema,
#     description="Обновление данных пользователя",
# )
# def update_user_handler(
#     user_id: int, first_name: str, last_name: str, date_of_birth: datetime
# ):
#     user_service = UserService()
#     return user_service.update_user(
#         user_id=user_id,
#         first_name=first_name,
#         last_name=last_name,
#         date_of_birth=date_of_birth,
#     )
#
#
# @router.delete(
#     "/{user_id}", response_model=UserResponseSchema, description="Удаление пользователя"
# )
# def delete_user_handler(user_id: int):
#     user_service = UserService()
#
#     try:
#         deleted_user = user_service.delete_user(user_id)
#     except ValidationException:
#         return HTTPException(
#             status_code=404, detail=f"Пользователь {user_id} не найден"
#         )
#     else:
#         return deleted_user
