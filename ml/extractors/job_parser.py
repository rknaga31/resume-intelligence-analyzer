"""
Job description parser — Milestone 7.

Extracts required, preferred, and optional skills from job descriptions
and identifies role requirements, experience level, and domain context.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from ml.extractors.skill_classifier import classify_skills


@dataclass
class ParsedJobDescription:
    """Structured output of job description parsing."""

    raw_required_skills: list[str] = field(default_factory=list)
    raw_preferred_skills: list[str] = field(default_factory=list)
    all_skills: list[str] = field(default_factory=list)
    experience_years_min: int | None = None
    experience_level: str = "mid"  # junior | mid | senior | lead | principal
    domain_keywords: list[str] = field(default_factory=list)
    responsibilities: list[str] = field(default_factory=list)


# Patterns for "required" vs "preferred" blocks in JDs
_REQUIRED_SECTION_RE = re.compile(
    r"(?:requirements?|required\s+qualifications?|must[\s-]have|"
    r"you\s+(?:will\s+have|must\s+have)|basic\s+qualifications?)"
    r"[\s:]+(.+?)(?=(?:preferred|nice[\s-]to[\s-]have|desired|optional|bonus|$))",
    re.IGNORECASE | re.DOTALL,
)

_PREFERRED_SECTION_RE = re.compile(
    r"(?:preferred\s+(?:qualifications?)?|nice[\s-]to[\s-]have|"
    r"desired|optional|bonus\s+if\s+you\s+have)"
    r"[\s:]+(.+?)(?=\n\n|\Z)",
    re.IGNORECASE | re.DOTALL,
)

_EXPERIENCE_RE = re.compile(
    r"(\d+)\+?\s*(?:to\s*\d+)?\s*years?\s+(?:of\s+)?(?:professional\s+)?experience",
    re.IGNORECASE,
)

_SENIORITY_LEVELS = {
    "principal": r"\b(?:principal|distinguished|fellow)\b",
    "lead": r"\b(?:tech lead|lead engineer|staff engineer|staff\s+\w+engineer)\b",
    "senior": r"\b(?:senior|sr\.?|sr\s)\b",
    "junior": r"\b(?:junior|jr\.?|jr\s|entry[\s-]level|associate)\b",
    "mid": r"\b(?:mid[\s-]level|engineer\s+ii|software engineer\s+ii)\b",
}


def parse_job_description(text: str) -> ParsedJobDescription:
    """Parse a job description into structured skill requirements.

    Args:
        text: Raw job description text.

    Returns:
        ParsedJobDescription with categorised skills and role context.
    """
    result = ParsedJobDescription()

    # Extract required skills section
    req_match = _REQUIRED_SECTION_RE.search(text)
    if req_match:
        req_text = req_match.group(1)
        result.raw_required_skills = classify_skills(req_text).raw_skills

    # Extract preferred skills section
    pref_match = _PREFERRED_SECTION_RE.search(text)
    if pref_match:
        pref_text = pref_match.group(1)
        result.raw_preferred_skills = classify_skills(pref_text).raw_skills

    # If no sections detected, classify full text
    if not result.raw_required_skills and not result.raw_preferred_skills:
        result.raw_required_skills = classify_skills(text).raw_skills

    result.all_skills = list(
        dict.fromkeys(result.raw_required_skills + result.raw_preferred_skills)
    )

    # Experience years
    exp_match = _EXPERIENCE_RE.search(text)
    if exp_match:
        result.experience_years_min = int(exp_match.group(1))

    # Seniority level
    text_lower = text.lower()
    for level, pattern in _SENIORITY_LEVELS.items():
        if re.search(pattern, text_lower):
            result.experience_level = level
            break

    # Extract bullet-point responsibilities (lines starting with - or •)
    result.responsibilities = [
        line.lstrip("-•* ").strip()
        for line in text.splitlines()
        if line.strip().startswith(("-", "•", "*")) and len(line.strip()) > 20
    ][:20]  # Cap at 20

    return result
