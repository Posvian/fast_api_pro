import pytest
from fastapi import status
from fastapi_pagination import response
from sqlalchemy import select

from src.account.models import Role


class TestUser:
    @pytest.mark.asyncio
    async def test_create_user(
        self,
        async_client,
        create_tables,
        get_user_payload,
        async_session,
        get_user_from_database,
        create_test_role,
    ):
        roles = await async_session.execute(
            select(Role).where(Role.name == "test_admin")
        )
        role = roles.scalars().one_or_none()
        data = get_user_payload
        data["role_id"] = role.id
        response = await async_client.post(
            "/api/v1/account/users/",
            json=data,
        )
        data_from_resp = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert data_from_resp["email"] == get_user_payload["email"]
        assert data_from_resp["first_name"] == get_user_payload["first_name"]
        assert data_from_resp["last_name"] == get_user_payload["last_name"]

        user_from_db = await get_user_from_database(data_from_resp["id"])
        assert user_from_db.first_name == get_user_payload["first_name"]
        assert user_from_db.last_name == get_user_payload["last_name"]
        assert user_from_db.email == get_user_payload["email"]
        assert user_from_db.is_active == True
        assert user_from_db.is_superuser == False
        assert user_from_db.role is not None
        assert user_from_db.role.name == "test_admin"

    @pytest.mark.asyncio
    async def test_create_duplicate_user(
        self,
        async_client,
        create_tables,
        get_user_payload,
        async_session,
    ):
        response = await async_client.post(
            "/api/v1/account/users/", json=get_user_payload
        )
        assert response.status_code == status.HTTP_201_CREATED
        response = await async_client.post(
            "/api/v1/account/users/", json=get_user_payload
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_list_users(
        self,
        async_client,
        create_tables,
        create_test_user,
        async_session,
        create_test_role,
    ):
        create_test_user.role = create_test_role
        response = await async_client.get(
            "/api/v1/account/users/",
        )
        assert response.status_code == status.HTTP_200_OK
        data_from_resp = response.json()
        assert len(data_from_resp) == 3
        assert data_from_resp["users"][0]["email"] == create_test_user.email
        assert data_from_resp["users"][0]["first_name"] == create_test_user.first_name

    @pytest.mark.asyncio
    async def test_get_user(
        self,
        async_client,
        create_tables,
        create_test_user,
        async_session,
        get_user_from_database,
    ):
        response = await async_client.get(
            f"/api/v1/account/users/{create_test_user.id}",
        )
        assert response.status_code == status.HTTP_200_OK
        data_from_resp = response.json()
        user_from_db = await get_user_from_database(data_from_resp["id"])
        assert data_from_resp["email"] == user_from_db.email
        assert data_from_resp["first_name"] == user_from_db.first_name
        assert data_from_resp["last_name"] == user_from_db.last_name

    @pytest.mark.asyncio
    async def test_update_user(
        self,
        async_client,
        create_tables,
        create_test_role,
        create_test_user,
        async_session,
        get_update_user_payload,
        get_user_from_database,
    ):
        response = await async_client.put(
            f"/api/v1/account/users/{create_test_user.id}",
            json=get_update_user_payload,
        )

        assert response.status_code == status.HTTP_200_OK
        data_from_resp = response.json()
        user_from_db = await get_user_from_database(data_from_resp["id"])
        assert user_from_db.role is not None
        assert user_from_db.first_name == get_update_user_payload["first_name"]
        assert user_from_db.last_name == get_update_user_payload["last_name"]
        assert user_from_db.role.id == get_update_user_payload["role_id"]
        assert user_from_db.role.name == create_test_role.name

    @pytest.mark.asyncio
    async def test_delete_user(
        self,
        async_client,
        create_tables,
        create_test_user,
        async_session,
    ):
        response = await async_client.delete(
            f"/api/v1/account/users/{create_test_user.id}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
