from typing import AsyncGenerator

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from showstock.auth import get_password_hash
from showstock.models.user import User


async def create_test_user(
    db: AsyncSession, username: str = "testuser", password: str = "testpass"
) -> User:
    """Create a test user in the database."""
    user = User(
        username=username,
        hashed_password=get_password_hash(password),
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


def get_auth_headers(client: TestClient, username: str, password: str) -> dict:
    """Get authentication headers for a test client."""
    response = client.post(
        "/auth/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
