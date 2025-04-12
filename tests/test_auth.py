import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from showstock.main import app
from tests.utils.auth import create_test_user, get_auth_headers


@pytest.mark.asyncio
async def test_login_success(client: TestClient, db: AsyncSession):
    """Test successful login."""
    # Create a test user
    await create_test_user(db, username="testuser", password="testpass")

    # Test login
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpass"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: TestClient, db: AsyncSession):
    """Test login with invalid credentials."""
    # Create a test user
    await create_test_user(db, username="testuser", password="testpass")

    # Test login with wrong password
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "wrongpass"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

    # Test login with non-existent user
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent", "password": "testpass"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


@pytest.mark.asyncio
async def test_auth_status(client: TestClient, db: AsyncSession):
    """Test authentication status endpoint."""
    # Create a test user
    user = await create_test_user(db, username="testuser", password="testpass")

    # Get auth headers
    headers = get_auth_headers(client, "testuser", "testpass")

    # Test auth status
    response = client.get("/auth/status", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["username"] == "testuser"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_auth_status_unauthorized(client: TestClient):
    """Test authentication status without token."""
    response = client.get("/auth/status")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_auth_status_invalid_token(client: TestClient):
    """Test authentication status with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/status", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


@pytest.mark.asyncio
async def test_logout(client: TestClient, db: AsyncSession):
    """Test logout endpoint."""
    # Create a test user
    await create_test_user(db, username="testuser", password="testpass")

    # Get auth headers
    headers = get_auth_headers(client, "testuser", "testpass")

    # Test logout
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"

    # Verify token is still valid (logout is client-side)
    response = client.get("/auth/status", headers=headers)
    assert response.status_code == 200
