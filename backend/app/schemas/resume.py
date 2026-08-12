"""
Pydantic schemas for resume-related API requests and responses.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class ResumeUploadResponse(BaseModel):
    """Response returned after a successful resume file upload."""

    file_id: str = Field(..., description="Unique identifier for the processed document")
    filename: str = Field(..., description="Sanitized filename (no path)")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="Detected MIME type")
    extracted_text: str = Field(..., description="Raw extracted text from the document")
    word_count: int = Field(..., description="Approximate word count of extracted text")
    character_count: int = Field(..., description="Character count of extracted text")
    extraction_method: str = Field(..., description="Library used for extraction")


class ParseResumeRequest(BaseModel):
    """Request body for parsing a resume into structured entities."""

    resume_text: str = Field(
        ...,
        min_length=50,
        max_length=50_000,
        description="Raw extracted resume text (50 - 50,000 characters)",
    )
    target_role: str | None = Field(
        None,
        max_length=200,
        description="Optional target job role for context",
    )
