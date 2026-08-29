"""
FastAPI application factory — Milestone 2.

Configures middleware, exception handlers, CORS, and mounts the API router.
"""
from __future__ import annotations

import time
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import (
    ResumeIntelligenceError,
    generic_exception_handler,
    resume_intelligence_exception_handler,
)
from app.core.logging import configure_logging, get_logger
from app.db.session import init_db

settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan — runs DB init on startup."""
    await init_db()
    logger.info("startup_complete", env=settings.app_env)
    yield
    logger.info("shutdown_complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Resume Intelligence Analyzer API — AI-powered resume parsing, "
            "semantic job matching, and explainable career recommendations."
        ),
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # -------------------------------------------------------------------------
    # CORS
    # -------------------------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # -------------------------------------------------------------------------
    # Request ID & Timing Middleware
    # -------------------------------------------------------------------------
    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next):  # type: ignore[return]
        """Attach a unique request ID and log request timing."""
        request_id = f"req_{uuid.uuid4().hex[:8]}"
        request.state.request_id = request_id
        start = time.perf_counter()

        response = await call_next(request)

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "http_request",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            elapsed_ms=elapsed_ms,
        )
        response.headers["X-Request-ID"] = request_id
        return response

    # -------------------------------------------------------------------------
    # Exception Handlers
    # -------------------------------------------------------------------------
    app.add_exception_handler(ResumeIntelligenceError, resume_intelligence_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # -------------------------------------------------------------------------
    # API Router
    # -------------------------------------------------------------------------
    app.include_router(api_router, prefix="/api/v1")

    # -------------------------------------------------------------------------
    # Root redirect to docs
    # -------------------------------------------------------------------------
    @app.get("/", include_in_schema=False)
    async def root() -> JSONResponse:
        return JSONResponse(
            {"message": "Resume Intelligence Analyzer API", "docs": "/docs", "version": settings.app_version}
        )

    logger.info(
        "app_started",
        version=settings.app_version,
        environment=settings.app_env,
    )

    return app


app = create_app()
