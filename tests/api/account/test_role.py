import pytest
from fastapi import status, HTTPException
from fastapi_pagination import response
from sqlalchemy import select

from src.account.models import Role


class TestRole:
    @pytest.mark.asyncio
    async def test_get_roles(
        self,
        async_client,
        create_tables,
        create_test_role,
        async_session,
        auth_headers_with_all_permissions,
    ):
        headers = auth_headers_with_all_permissions
        response = await async_client.get("/api/v1/account/roles/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data_from_resp = response.json()

        result = await async_session.execute(select(Role))
        roles_in_db = result.scalars().all()

        assert len(data_from_resp) == 3
        assert data_from_resp["count_of_pages"] == 1
        assert data_from_resp["count_of_roles"] == len(roles_in_db)
        assert data_from_resp["roles"][0]["name"] == create_test_role.name

    @pytest.mark.asyncio
    async def test_get_role(
        self,
        async_client,
        create_tables,
        create_test_role,
        async_session,
        get_role_from_database,
    ):
        response = await async_client.get(
            f"/api/v1/account/roles/{create_test_role.id}"
        )
        assert response.status_code == status.HTTP_200_OK
        data_from_resp = response.json()
        assert data_from_resp["name"] == create_test_role.name
        role_from_db = await get_role_from_database(data_from_resp["id"])
        assert data_from_resp["name"] == role_from_db.name

    @pytest.mark.asyncio
    async def test_create_role(
        self,
        async_client,
        create_tables,
        get_role_payload,
        async_session,
        get_role_from_database,
    ):
        response = await async_client.post(
            "/api/v1/account/roles/",
            json=get_role_payload,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data_from_resp = response.json()
        assert data_from_resp["name"] == get_role_payload["name"]
        role_from_db = await get_role_from_database(role_id=data_from_resp["id"])
        assert data_from_resp["name"] == role_from_db.name

    @pytest.mark.asyncio
    async def test_delete_role(
        self,
        async_client,
        create_tables,
        create_test_role,
        async_session,
        get_role_from_database,
    ):

        response = await async_client.delete(
            f"/api/v1/account/roles/{create_test_role.id}"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(HTTPException):
            await get_role_from_database(role_id=create_test_role.id)
