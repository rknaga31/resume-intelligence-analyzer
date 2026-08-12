"""
Structured, zero-PII logging for the Resume Intelligence Analyzer.

Usage:
    from app.core.logging import get_logger
    logger = get_logger(__name__)
    logger.info("resume_parsed", request_id=req_id, word_count=520)

Rules:
    - NEVER log: candidate names, emails, phone numbers, resume text, PII.
    - ALWAYS log: request_id, event name, timing, status codes, error types.
"""
from __future__ import annotations

import logging
import sys
from typing import Any

import structlog


def configure_logging(log_level: str = "INFO") -> None:
    """Configure structlog with JSON rendering for production, pretty for dev."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.ExceptionRenderer(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(sys.stdout),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> Any:
    """Return a bound structlog logger for the given module name.

    Args:
        name: Module name (pass ``__name__``).

    Returns:
        A structlog BoundLogger instance.
    """
    return structlog.get_logger(name)


# Module-level logger for import convenience.
logger = get_logger(__name__)
