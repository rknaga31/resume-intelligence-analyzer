"""
Pydantic schemas for analysis API requests and responses.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class FullAnalysisRequest(BaseModel):
    """Request body for a complete end-to-end resume intelligence analysis."""

    resume_text: str = Field(
        ...,
        min_length=50,
        max_length=50_000,
        description="Extracted resume text",
    )
    target_role: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Target job role (e.g. 'Senior AI Engineer')",
    )
    job_description: str | None = Field(
        None,
        max_length=20_000,
        description="Optional full job description text",
    )


class SkillMatch(BaseModel):
    """Represents a matched skill between resume and job description."""

    resume_skill: str
    job_skill: str
    similarity: float = Field(..., ge=0.0, le=1.0)


class BulletFeedback(BaseModel):
    """Feedback on a single experience bullet point."""

    original: str
    issue: str
    suggestion: str


class AchievementAnalysis(BaseModel):
    """Quantification analysis across all experience bullet points."""

    quantified_bullets_count: int
    total_bullets_count: int
    quantification_rate: float = Field(..., ge=0.0, le=1.0)
    bullet_feedback: list[BulletFeedback] = Field(default_factory=list)


class ScoreBreakdown(BaseModel):
    """Multi-dimensional scoring with evidence and reasoning."""

    overall_score: int = Field(..., ge=0, le=100)
    ats_compatibility_score: int = Field(..., ge=0, le=100)
    job_match_score: int = Field(..., ge=0, le=100)
    achievement_impact_score: int = Field(..., ge=0, le=100)
    skill_relevance_score: int = Field(..., ge=0, le=100)
    ats_disclaimer: str = (
        "This is an AI-assisted ATS-style analysis and does not guarantee "
        "the behavior of a specific employer's proprietary ATS system."
    )


class SkillBreakdown(BaseModel):
    """Skill classification result."""

    matched: list[str] = Field(default_factory=list)
    partial: list[SkillMatch] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)
    resume_skills: list[str] = Field(default_factory=list)


class LLMSynthesis(BaseModel):
    """Structured LLM-generated analysis output."""

    executive_summary: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    actionable_recommendations: list[str] = Field(default_factory=list)
    career_roadmap: list[str] = Field(default_factory=list)
    provider_used: str = "fallback"


class FullAnalysisResponse(BaseModel):
    """Complete end-to-end analysis response."""

    analysis_id: str
    target_role: str
    scores: ScoreBreakdown
    skills: SkillBreakdown
    sections_found: list[str] = Field(default_factory=list)
    achievement_analysis: AchievementAnalysis
    llm_synthesis: LLMSynthesis
