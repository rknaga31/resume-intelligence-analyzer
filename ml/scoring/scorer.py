"""
Master scoring orchestrator — Milestone 9.

Combines ATS analysis, achievement impact, and skill match
to produce multi-dimensional explainable resume scores.

Scoring dimensions and weights:
  - ATS Compatibility: 25%
  - Job Match (skills + semantic): 35%
  - Achievement Impact: 25%
  - Skill Relevance: 15%
"""
from __future__ import annotations

from dataclasses import dataclass

from ml.extractors.skill_classifier import classify_skills, match_skills_to_job
from ml.extractors.job_parser import parse_job_description
from ml.parsers.section_detector import get_section_names
from ml.scoring.ats_analyzer import compute_ats_score, ATSScoreResult
from ml.scoring.achievement_analyzer import analyze_achievements, AchievementAnalysisResult


@dataclass
class ScoringResult:
    """Complete multi-dimensional scoring output."""

    overall_score: int
    ats_score: int
    job_match_score: int
    achievement_score: int
    skill_relevance_score: int
    ats_result: ATSScoreResult
    achievement_result: AchievementAnalysisResult
    skill_match: dict
    resume_skills: list[str]
    job_skills: list[str]
    sections_found: list[str]


def score_resume(
    resume_text: str,
    target_role: str,
    job_description: str | None = None,
) -> ScoringResult:
    """Orchestrate multi-dimensional resume scoring.

    Args:
        resume_text: Full extracted resume text.
        target_role: Target job role string.
        job_description: Optional full job description text.

    Returns:
        ScoringResult with all score dimensions and supporting evidence.
    """
    # 1. ATS Analysis (25%)
    ats_result = compute_ats_score(resume_text)
    ats_score = ats_result.score

    # 2. Skill Extraction from resume
    resume_classification = classify_skills(resume_text)
    resume_skills = resume_classification.raw_skills

    # 3. Job skill extraction
    if job_description:
        parsed_job = parse_job_description(job_description)
        job_skills = parsed_job.all_skills
    else:
        # If no JD, extract skills from target role name as proxy
        parsed_job = parse_job_description(target_role)
        job_skills = parsed_job.all_skills

    # 4. Skill matching
    skill_match = match_skills_to_job(resume_skills, job_skills)
    skill_relevance_score = _compute_skill_relevance(resume_skills)

    # 5. Job match score (keyword + skill coverage)
    job_match_score = _compute_job_match_score(skill_match, job_skills)

    # 6. Achievement impact
    achievement_result = analyze_achievements(resume_text)
    achievement_score = achievement_result.score

    # 7. Section detection
    sections_found = get_section_names(resume_text)

    # 8. Weighted overall score
    overall_score = int(
        ats_score * 0.25
        + job_match_score * 0.35
        + achievement_score * 0.25
        + skill_relevance_score * 0.15
    )

    return ScoringResult(
        overall_score=min(overall_score, 100),
        ats_score=ats_score,
        job_match_score=job_match_score,
        achievement_score=achievement_score,
        skill_relevance_score=skill_relevance_score,
        ats_result=ats_result,
        achievement_result=achievement_result,
        skill_match=skill_match,
        resume_skills=resume_skills,
        job_skills=job_skills,
        sections_found=sections_found,
    )


def _compute_job_match_score(skill_match: dict, job_skills: list[str]) -> int:
    """Compute job match score from skill coverage.

    Args:
        skill_match: Output of match_skills_to_job.
        job_skills: All required job skills.

    Returns:
        Job match score 0-100.
    """
    if not job_skills:
        return 50  # No JD provided — neutral score

    total = len(job_skills)
    matched_pts = len(skill_match.get("matched", [])) * 1.0
    partial_pts = len(skill_match.get("partial", [])) * 0.6

    coverage = (matched_pts + partial_pts) / total if total > 0 else 0.0
    return min(int(coverage * 100), 100)


def _compute_skill_relevance(resume_skills: list[str]) -> int:
    """Score skill breadth and depth (proxy: unique taxonomy category count).

    Args:
        resume_skills: Canonical skill names from resume.

    Returns:
        Skill relevance score 0-100.
    """
    from ml.extractors.skill_classifier import _load_taxonomy  # noqa: PLC0415

    taxonomy = _load_taxonomy()
    categories_hit: set[str] = set()

    for cat_name, cat_data in taxonomy["categories"].items():
        for canonical_skill in cat_data["skills"]:
            if canonical_skill in resume_skills:
                categories_hit.add(cat_name)

    # Each category adds ~8 points, capped at 100
    return min(len(categories_hit) * 8, 100)
