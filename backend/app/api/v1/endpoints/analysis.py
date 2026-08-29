"""
Full analysis endpoint — Milestone 9 + 10.

Orchestrates the complete intelligence pipeline:
  Document extraction → Section detection → Skill classification →
  ATS analysis → Achievement analysis → Scoring → LLM synthesis → Response
"""
from __future__ import annotations

import uuid

from fastapi import APIRouter

from app.schemas.analysis import (
    AchievementAnalysis,
    BulletFeedback,
    FullAnalysisRequest,
    FullAnalysisResponse,
    LLMSynthesis,
    ScoreBreakdown,
    SkillBreakdown,
    SkillMatch,
)
from ml.llm.reasoner import synthesize_analysis
from ml.scoring.scorer import score_resume

router = APIRouter()


@router.post(
    "/full",
    response_model=FullAnalysisResponse,
    summary="Full Resume Intelligence Analysis",
    description=(
        "Run the complete AI/ML pipeline: section detection, entity extraction, "
        "skill taxonomy classification, ATS-style scoring, achievement impact analysis, "
        "and LLM-powered recommendations. "
        "All resume content is treated as untrusted input with prompt injection defense."
    ),
)
async def full_analysis(request: FullAnalysisRequest) -> FullAnalysisResponse:
    """Run end-to-end resume intelligence analysis.

    Args:
        request: FullAnalysisRequest with resume_text, target_role, and optional job_description.

    Returns:
        FullAnalysisResponse with multi-dimensional scores, skill breakdown, and recommendations.
    """
    # 1. Score the resume (deterministic pipeline)
    scoring = score_resume(
        resume_text=request.resume_text,
        target_role=request.target_role,
        job_description=request.job_description,
    )

    # 2. LLM synthesis (with fallback)
    achievement_issues = [
        b.suggestion or ""
        for b in scoring.achievement_result.bullets
        if not b.is_quantified and b.suggestion
    ][:5]

    llm_output = synthesize_analysis(
        resume_text=request.resume_text,
        target_role=request.target_role,
        skill_match=scoring.skill_match,
        ats_issues=scoring.ats_result.issues,
        achievement_issues=achievement_issues,
    )

    # 3. Build response
    scores = ScoreBreakdown(
        overall_score=scoring.overall_score,
        ats_compatibility_score=scoring.ats_score,
        job_match_score=scoring.job_match_score,
        achievement_impact_score=scoring.achievement_score,
        skill_relevance_score=scoring.skill_relevance_score,
    )

    skills = SkillBreakdown(
        matched=scoring.skill_match.get("matched", []),
        partial=[
            SkillMatch(
                resume_skill=p["resume_skill"],
                job_skill=p["job_skill"],
                similarity=p["similarity"],
            )
            for p in scoring.skill_match.get("partial", [])
        ],
        missing=scoring.skill_match.get("missing", []),
        resume_skills=scoring.resume_skills,
    )

    achievement_analysis = AchievementAnalysis(
        quantified_bullets_count=scoring.achievement_result.quantified_count,
        total_bullets_count=scoring.achievement_result.total_count,
        quantification_rate=scoring.achievement_result.quantification_rate,
        bullet_feedback=[
            BulletFeedback(
                original=b.text[:200],
                issue=b.issue or "",
                suggestion=b.suggestion or "",
            )
            for b in scoring.achievement_result.bullets
            if not b.is_quantified and b.issue
        ][:8],
    )

    llm_synthesis = LLMSynthesis(
        executive_summary=llm_output.executive_summary,
        strengths=llm_output.strengths,
        weaknesses=llm_output.weaknesses,
        actionable_recommendations=llm_output.actionable_recommendations,
        career_roadmap=llm_output.career_roadmap,
        provider_used=llm_output.provider_used,
    )

    return FullAnalysisResponse(
        analysis_id=f"an_{uuid.uuid4().hex[:8]}",
        target_role=request.target_role,
        scores=scores,
        skills=skills,
        sections_found=scoring.sections_found,
        achievement_analysis=achievement_analysis,
        llm_synthesis=llm_synthesis,
    )
