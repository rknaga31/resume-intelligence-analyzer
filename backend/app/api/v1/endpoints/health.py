"""Health check endpoint."""
from __future__ import annotations

import platform
import sys
from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get(
    "/health",
    summary="Health Check",
    description="Returns system status, version, and runtime information.",
    tags=["System"],
)
async def health_check() -> dict:
    """Return application health status.

    Returns:
        JSON payload with status, version, environment, and timestamp.
    """
    settings = get_settings()
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "timestamp": datetime.now(UTC).isoformat(),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": platform.system(),
    }
