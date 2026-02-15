import pytest


class TestAuth:
    @pytest.mark.asyncio
    async def test_register(self, async_client):
        response = await async_client.post(
            "/api/v1/authentication/jwt/register",
            json={"email": "test@test.com", "password": "123456789"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
