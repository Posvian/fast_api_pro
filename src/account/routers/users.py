from datetime import datetime
from typing import Union

from fastapi import APIRouter, HTTPException
from fastapi.exceptions import ValidationException, ResponseValidationError

from account.schemas import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from account.servicies import UserService

router = APIRouter(prefix="/users", tags=["ACCOUNT"])


@router.post("/", response_model=UserCreateSchema)
def create_user_handler(payload: UserCreateSchema):
    return payload


@router.get("/", response_model=list[UserResponseSchema])
def get_users_handler():
    user_service = UserService()
    return user_service.get_user_list()


@router.put("/{user_id}", response_model=UserUpdateSchema)
def update_user_handler(
    user_id: int, first_name: str, last_name: str, date_of_birth: datetime
):
    user_service = UserService()
    return user_service.update_user(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
    )


@router.delete("/{user_id}", response_model=UserResponseSchema)
def delete_user_handler(user_id: int):
    user_service = UserService()

    try:
        deleted_user = user_service.delete_user(user_id)
    except ValidationException:
        return HTTPException(
            status_code=404, detail=f"Пользователь {user_id} не найден"
        )
    else:
        return deleted_user
