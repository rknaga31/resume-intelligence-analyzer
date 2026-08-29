"""
Integration tests for authentication API endpoints.

Uses FastAPI TestClient with an in-memory SQLite database per module.
"""
from __future__ import annotations

import asyncio

import pytest
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

_TEST_EMAIL = "auth_test@example.com"
_TEST_PASSWORD = "Str0ngP@ssword!"


# ---------------------------------------------------------------------------
# Module-scoped client fixture using asyncio.run for setup/teardown
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def auth_client():
    """TestClient with a fresh in-memory SQLite DB, shared across this module."""
    engine = create_async_engine(
        TEST_DB_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    # Create all tables
    async def _setup() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.get_event_loop().run_until_complete(_setup())

    async def override_get_db():
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

    async def _teardown() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

    asyncio.get_event_loop().run_until_complete(_teardown())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRegister:
    def test_register_new_user_success(self, auth_client: TestClient) -> None:
        response = auth_client.post(
            "/api/v1/auth/register",
            json={"email": _TEST_EMAIL, "password": _TEST_PASSWORD},
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["email"] == _TEST_EMAIL
        assert data["is_active"] is True
        assert "id" in data
        assert "hashed_password" not in data

    def test_register_duplicate_email_returns_409(self, auth_client: TestClient) -> None:
        response = auth_client.post(
            "/api/v1/auth/register",
            json={"email": _TEST_EMAIL, "password": _TEST_PASSWORD},
        )
        assert response.status_code == 409

    def test_register_weak_password_returns_422(self, auth_client: TestClient) -> None:
        response = auth_client.post(
            "/api/v1/auth/register",
            json={"email": "newuser@example.com", "password": "short"},
        )
        assert response.status_code == 422


class TestLogin:
    def test_login_valid_credentials_returns_tokens(self, auth_client: TestClient) -> None:
        response = auth_client.post(
            "/api/v1/auth/login",
            json={"email": _TEST_EMAIL, "password": _TEST_PASSWORD},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0

    def test_login_wrong_password_returns_401(self, auth_client: TestClient) -> None:
        response = auth_client.post(
            "/api/v1/auth/login",
            json={"email": _TEST_EMAIL, "password": "WrongPassword!"},
        )
        assert response.status_code == 401

    def test_login_unknown_email_returns_401(self, auth_client: TestClient) -> None:
        response = auth_client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@nowhere.com", "password": "anything"},
        )
        assert response.status_code == 401


class TestGetMe:
    def _get_token(self, client: TestClient) -> str:
        """Helper: login and return a fresh access token."""
        r = client.post(
            "/api/v1/auth/login",
            json={"email": _TEST_EMAIL, "password": _TEST_PASSWORD},
        )
        assert r.status_code == 200
        return r.json()["access_token"]

    def test_get_me_with_valid_token(self, auth_client: TestClient) -> None:
        token = self._get_token(auth_client)
        response = auth_client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == _TEST_EMAIL
        assert "hashed_password" not in data

    def test_get_me_without_token_returns_401(self, auth_client: TestClient) -> None:
        response = auth_client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_get_me_with_invalid_token_returns_401(self, auth_client: TestClient) -> None:
        response = auth_client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer this.is.not.valid"},
        )
        assert response.status_code == 401
