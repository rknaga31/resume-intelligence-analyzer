"""
Pydantic schemas for authentication endpoints.
"""
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Request body for creating a new user account."""

    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password (minimum 8 characters)",
    )


class LoginRequest(BaseModel):
    """Request body for obtaining JWT tokens."""

    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., description="Account password")


class TokenResponse(BaseModel):
    """JWT token pair returned after successful authentication."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Access token lifetime in seconds")


class RefreshRequest(BaseModel):
    """Request body for refreshing an access token."""

    refresh_token: str


class UserResponse(BaseModel):
    """Public user profile — no password or sensitive data."""

    id: str
    email: str
    is_active: bool
    is_verified: bool
    created_at: str

    model_config = {"from_attributes": True}
