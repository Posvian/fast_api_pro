from datetime import datetime
from fastapi.exceptions import ValidationException

from account.schemas import UserResponseSchema, UserUpdateSchema

users = [
    {
        "id": 1,
        "email": "string",
        "last_name": "string",
        "date_of_birth": "2025-06-22T07:16:11.323Z",
    },
    {
        "id": 2,
        "email": "string",
        "first_name": "string",
        "date_of_birth": "2025-06-22T07:16:11.323Z",
    },
    {
        "id": 3,
        "email": "string",
        "first_name": "string",
        "last_name": "string",
    },
]


class UserService:
    def get_user_list(self) -> list[UserResponseSchema]:
        data: list[UserResponseSchema] = [UserResponseSchema(**item) for item in users]
        return data

    def get_user(self, user_id: int) -> UserResponseSchema | None:
        user_list: list[UserResponseSchema] = self.get_user_list()
        for user in user_list:
            if user.id == user_id:
                return user
        return None

    def update_user(
        self, user_id: int, first_name: str, last_name: str, date_of_birth: datetime
    ) -> UserUpdateSchema:

        user_data = None
        for user in users:
            if user["id"] == user_id:
                user_data = user
                break

        if not user_data:
            raise ValidationException(f"Пользователя с {user_id} не существует!")

        user_data.update(
            {
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": date_of_birth,
            }
        )

        return UserUpdateSchema(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )

    def delete_user(self, user_id: int) -> UserResponseSchema:
        user_data = None
        for i in range(len(users)):
            if users[i]["id"] == user_id:
                user_data = users.pop(i)
                break

        if not user_data:
            raise ValidationException(f"Пользователя с {user_id} не существует!")

        return UserResponseSchema.model_validate(user_data)
