"""
LLM Reasoning Orchestrator — Milestone 10.

Selects the configured LLM provider and produces validated synthesis output.
Graceful fallback to rule-based provider on any API failure.
"""
from __future__ import annotations

from app.core.config import get_settings
from app.core.logging import get_logger

from ml.llm.base import BaseLLMProvider, LLMAnalysisOutput
from ml.llm.fallback_provider import FallbackProvider

logger = get_logger(__name__)


def _get_provider() -> BaseLLMProvider:
    """Return the configured LLM provider.

    Provider selection is read from LLM_PROVIDER env var.
    Falls back to rule-based if API key is not configured.

    Returns:
        Configured BaseLLMProvider implementation.
    """
    settings = get_settings()

    if settings.llm_provider == "gemini" and settings.google_api_key:
        from ml.llm.gemini_provider import GeminiProvider  # noqa: PLC0415
        return GeminiProvider(
            api_key=settings.google_api_key,
            model=settings.google_gemini_model,
        )

    if settings.llm_provider == "openai" and settings.openai_api_key:
        try:
            from ml.llm.openai_provider import OpenAIProvider  # noqa: PLC0415
            return OpenAIProvider()
        except ImportError:
            logger.warning("openai_import_error", fallback="rule-based")

    if settings.llm_provider == "anthropic" and settings.anthropic_api_key:
        try:
            from ml.llm.anthropic_provider import AnthropicProvider  # noqa: PLC0415
            return AnthropicProvider()
        except ImportError:
            logger.warning("anthropic_import_error", fallback="rule-based")

    return FallbackProvider()


def synthesize_analysis(
    resume_text: str,
    target_role: str,
    skill_match: dict,
    ats_issues: list[str],
    achievement_issues: list[str],
) -> LLMAnalysisOutput:
    """Run LLM-powered analysis synthesis with automatic fallback.

    Args:
        resume_text: Full resume text (treated as untrusted by all providers).
        target_role: Target job role string.
        skill_match: Skill matching results from scoring engine.
        ats_issues: ATS compatibility issues.
        achievement_issues: Bullet improvement suggestions.

    Returns:
        Validated LLMAnalysisOutput.
    """
    provider = _get_provider()
    logger.info("llm_synthesis_started", provider=provider.provider_name)

    try:
        result = provider.synthesize(
            resume_text=resume_text,
            target_role=target_role,
            skill_match=skill_match,
            ats_issues=ats_issues,
            achievement_issues=achievement_issues,
        )
        logger.info("llm_synthesis_complete", provider=provider.provider_name)
        return result
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "llm_synthesis_error",
            provider=provider.provider_name,
            error_type=type(exc).__name__,
            fallback="rule-based",
        )
        return FallbackProvider().synthesize(
            resume_text=resume_text,
            target_role=target_role,
            skill_match=skill_match,
            ats_issues=ats_issues,
            achievement_issues=achievement_issues,
        )
