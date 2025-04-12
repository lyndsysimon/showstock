from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """JWT token response schema."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT token data schema."""

    username: Optional[str] = None


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    username: str
    is_active: bool
