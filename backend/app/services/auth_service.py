"""
Authentication service — user registration, login, and token validation.

All DB interactions go through this service; route handlers stay thin.
"""
from __future__ import annotations

from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    settings,
    verify_password,
)
from app.db.models.user import User
from app.db.session import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)
_bearer = HTTPBearer(auto_error=False)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


async def register_user(db: AsyncSession, email: str, password: str) -> User:
    """Create a new user account.

    Args:
        db: Async database session.
        email: New user's email (must be unique).
        password: Plain-text password (will be hashed).

    Returns:
        Newly created User ORM object.

    Raises:
        HTTPException 409: If the email is already registered.
    """
    email = email.lower().strip()
    existing = await db.scalar(select(User).where(User.email == email))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "USER_ALREADY_EXISTS", "message": "Email is already registered."},
        )
    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)
    await db.flush()  # Get the generated ID before commit
    logger.info("user_registered", user_id=user.id)
    return user


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    """Verify email + password and return the User.

    Args:
        db: Async database session.
        email: Candidate email.
        password: Plain-text password.

    Returns:
        Authenticated User ORM object.

    Raises:
        HTTPException 401: If credentials are invalid or account is inactive.
    """
    email = email.lower().strip()
    user = await db.scalar(select(User).where(User.email == email))

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Incorrect email or password."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCOUNT_INACTIVE", "message": "This account has been deactivated."},
        )
    logger.info("user_logged_in", user_id=user.id)
    return user


def issue_tokens(user_id: str) -> dict[str, str | int]:
    """Issue an access + refresh token pair for the given user ID.

    Args:
        user_id: The user's primary key.

    Returns:
        Dict with access_token, refresh_token, token_type, expires_in.
    """
    return {
        "access_token": create_access_token(subject=user_id),
        "refresh_token": create_refresh_token(subject=user_id),
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
    }


# ---------------------------------------------------------------------------
# Protected route dependency
# ---------------------------------------------------------------------------


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    """FastAPI dependency that validates a Bearer token and returns the user.

    Args:
        credentials: HTTP Authorization header bearer token.
        db: Async database session.

    Returns:
        The authenticated User ORM object.

    Raises:
        HTTPException 401: If the token is missing, invalid, or expired.
        HTTPException 403: If the account is inactive.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "MISSING_TOKEN", "message": "Authentication token required."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_token(credentials.credentials)
        user_id: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")
        if not user_id or token_type != "access":
            raise JWTError("invalid token type")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "Token is invalid or expired."},
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "USER_NOT_FOUND", "message": "User account not found."},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCOUNT_INACTIVE", "message": "Account deactivated."},
        )
    return user
