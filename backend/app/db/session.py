"""
Async database session management.

Usage (in FastAPI endpoints):
    async def my_endpoint(db: AsyncSession = Depends(get_db)):
        ...
"""
from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

settings = get_settings()

# Create the async engine.
# In development: sqlite+aiosqlite:///./resume_intelligence.db
# In production:  postgresql+asyncpg://user:pass@host/db
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
    # SQLite-specific: needed to avoid "check same thread" errors
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async DB session per request.

    Yields:
        AsyncSession: The SQLAlchemy async session for this request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Create all tables (dev / test only — use Alembic in production).

    This is called on application startup when running in development mode.
    """
    import app.db.models  # noqa: F401 — register all models with Base metadata
    from app.db.base import Base  # noqa: F401 — ensure models are imported

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("database_initialized", url=settings.database_url.split("@")[-1])
