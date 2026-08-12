"""API v1 router — aggregates all endpoint sub-routers."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import health, resumes, analysis

api_router = APIRouter()

api_router.include_router(health.router, prefix="", tags=["System"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
api_router.include_router(analysis.router, prefix="/analyze", tags=["Analysis"])
