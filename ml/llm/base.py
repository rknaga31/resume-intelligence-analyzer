"""
Abstract LLM provider base — Milestone 10.

All LLM calls go through this abstraction layer.
Adapters for OpenAI, Anthropic, Gemini, and rule-based fallback
implement this interface.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMAnalysisOutput:
    """Structured, validated LLM synthesis output."""

    executive_summary: str
    strengths: list[str]
    weaknesses: list[str]
    actionable_recommendations: list[str]
    career_roadmap: list[str]
    provider_used: str


class BaseLLMProvider(ABC):
    """Abstract base class for LLM provider adapters."""

    provider_name: str = "base"

    @abstractmethod
    def synthesize(
        self,
        resume_text: str,
        target_role: str,
        skill_match: dict,
        ats_issues: list[str],
        achievement_issues: list[str],
    ) -> LLMAnalysisOutput:
        """Generate structured career analysis and recommendations.

        Args:
            resume_text: UNTRUSTED — resume text wrapped in sandbox tags by provider.
            target_role: Target job role.
            skill_match: Matched/partial/missing skill dictionary.
            ats_issues: List of ATS compatibility issues.
            achievement_issues: List of bullet point improvement suggestions.

        Returns:
            Validated LLMAnalysisOutput.
        """
        ...
