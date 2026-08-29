"""Auth endpoints — register, login, token refresh, and user profile."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth_service import authenticate_user, get_current_user, issue_tokens, register_user

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Register a new user account",
    description="Create a new account with email and password. Returns the created user profile.",
)
async def register(
    body: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Register a new user.

    Args:
        body: RegisterRequest with email and password.
        db: Async database session.

    Returns:
        UserResponse with the created user's public profile.
    """
    user = await register_user(db, email=body.email, password=body.password)
    return UserResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at.isoformat(),
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and obtain JWT tokens",
    description="Authenticate with email and password. Returns an access token and refresh token.",
)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Authenticate and issue tokens.

    Args:
        body: LoginRequest with email and password.
        db: Async database session.

    Returns:
        TokenResponse containing access and refresh JWTs.
    """
    user = await authenticate_user(db, email=body.email, password=body.password)
    tokens = issue_tokens(user.id)
    return TokenResponse(**tokens)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh an expired access token",
    description="Provide a valid refresh token to receive a new access token pair.",
)
async def refresh_token(body: RefreshRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Exchange a refresh token for a new access + refresh pair.

    Args:
        body: RefreshRequest containing the refresh token.
        db: Async database session.

    Returns:
        TokenResponse with new token pair.
    """
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise JWTError("wrong token type")
        user_id: str = payload["sub"]
    except (JWTError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_REFRESH_TOKEN", "message": "Refresh token is invalid or expired."},
        )
    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive.")
    tokens = issue_tokens(user.id)
    return TokenResponse(**tokens)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the authenticated user's public profile. Requires a valid Bearer token.",
)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return the authenticated user's profile.

    Args:
        current_user: Injected via the get_current_user dependency.

    Returns:
        UserResponse with public profile fields.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at.isoformat(),
    )
