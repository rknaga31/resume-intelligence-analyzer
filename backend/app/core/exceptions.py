"""
Custom exception classes and FastAPI exception handlers.

All error responses follow RFC 7807 Problem Details format.
Internal details are never leaked to clients in production.
"""
from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logging import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Domain Exceptions
# ---------------------------------------------------------------------------


class ResumeIntelligenceError(Exception):
    """Base exception for all application errors."""

    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"

    def __init__(self, message: str, details: dict | None = None) -> None:
        """Initialise the exception.

        Args:
            message: Human-readable error message.
            details: Optional dictionary with extra context (never PII).
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class DocumentProcessingError(ResumeIntelligenceError):
    """Raised when a resume document cannot be processed."""

    status_code = 422
    error_code = "DOCUMENT_PROCESSING_ERROR"


class UnsupportedFileTypeError(ResumeIntelligenceError):
    """Raised when the uploaded file type is not supported."""

    status_code = 400
    error_code = "UNSUPPORTED_FILE_TYPE"


class FileTooLargeError(ResumeIntelligenceError):
    """Raised when the uploaded file exceeds the size limit."""

    status_code = 413
    error_code = "FILE_TOO_LARGE"


class EmptyDocumentError(ResumeIntelligenceError):
    """Raised when the extracted document text is empty or too short."""

    status_code = 422
    error_code = "EMPTY_DOCUMENT"


class LLMProviderError(ResumeIntelligenceError):
    """Raised when the configured LLM provider fails."""

    status_code = 503
    error_code = "LLM_PROVIDER_ERROR"


class ValidationError(ResumeIntelligenceError):
    """Raised when request payload validation fails."""

    status_code = 400
    error_code = "VALIDATION_ERROR"


# ---------------------------------------------------------------------------
# Exception Handlers
# ---------------------------------------------------------------------------


def _build_error_response(
    request: Request,
    status_code: int,
    error_code: str,
    message: str,
    details: dict | None = None,
) -> JSONResponse:
    """Build a standardised RFC 7807 JSON error response.

    Args:
        request: The incoming FastAPI request.
        status_code: HTTP status code.
        error_code: Machine-readable error identifier.
        message: Human-readable description.
        details: Optional non-PII context dictionary.

    Returns:
        JSONResponse with error payload.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(
        "request_error",
        request_id=request_id,
        error_code=error_code,
        status_code=status_code,
        path=str(request.url.path),
    )
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "message": message,
                "details": details,
                "request_id": request_id,
            }
        },
    )


async def resume_intelligence_exception_handler(
    request: Request, exc: ResumeIntelligenceError
) -> JSONResponse:
    """Handle all ResumeIntelligenceError subclasses."""
    return _build_error_response(
        request,
        exc.status_code,
        exc.error_code,
        exc.message,
        exc.details if exc.details else None,
    )


async def generic_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions without leaking internal details."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        "unhandled_exception",
        request_id=request_id,
        exc_info=True,
        path=str(request.url.path),
    )
    return _build_error_response(
        request,
        500,
        "INTERNAL_SERVER_ERROR",
        "An unexpected error occurred. Please try again later.",
    )
