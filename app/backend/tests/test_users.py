import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register
        response = await ac.post("/api/auth/register", json={"email": "test@example.com", "password": "testpass"})
        assert response.status_code == 200
        # Login
        response = await ac.post("/api/auth/login", json={"email": "test@example.com", "password": "testpass"})
        assert response.status_code == 200
        assert "access_token" in response.json()
