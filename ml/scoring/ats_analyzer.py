"""
ATS-Style Compatibility Analyzer — Milestone 9.

Produces an ATS compatibility score based on deterministic rules:
- Contact information completeness
- Standard section header presence
- Formatting quality
- Date consistency
- Content length sanity

DISCLAIMER: This is an AI-assisted ATS-style analysis and does not guarantee
the behavior of any specific employer's proprietary ATS system.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from ml.extractors.contact import extract_contact_info
from ml.parsers.section_detector import get_section_names

_ATS_DISCLAIMER = (
    "This is an AI-assisted ATS-style analysis and does not guarantee "
    "the behavior of a specific employer's proprietary ATS system."
)


@dataclass
class ATSScoreResult:
    """Detailed ATS compatibility score with evidence."""

    score: int
    disclaimer: str = _ATS_DISCLAIMER
    components: dict[str, int] = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)


def _score_contact_info(text: str) -> tuple[int, list[str], list[str]]:
    """Score contact information completeness (max 25 points)."""
    contact = extract_contact_info(text)
    score = 0
    issues: list[str] = []
    strengths: list[str] = []

    if contact.get("email"):
        score += 10
        strengths.append("Email address detected")
    else:
        issues.append("No email address found — critical for ATS parsing")

    if contact.get("phone"):
        score += 5
        strengths.append("Phone number detected")
    else:
        issues.append("No phone number found")

    if contact.get("location"):
        score += 5
        strengths.append("Location detected")
    else:
        issues.append("No location found — some ATS systems require it")

    if contact.get("linkedin") or contact.get("github"):
        score += 5
        strengths.append("Professional profile URL detected")

    return score, issues, strengths


def _score_sections(text: str) -> tuple[int, list[str], list[str]]:
    """Score standard section header presence (max 35 points)."""
    sections = get_section_names(text)
    score = 0
    issues: list[str] = []
    strengths: list[str] = []

    section_points = {
        "Experience": (10, "Work Experience section detected"),
        "Skills": (10, "Skills section detected"),
        "Education": (10, "Education section detected"),
        "Summary": (5, "Professional Summary/Objective detected"),
    }

    for section, (pts, strength_msg) in section_points.items():
        if section in sections:
            score += pts
            strengths.append(strength_msg)
        else:
            issues.append(f"No '{section}' section found — ATS may struggle to categorize your experience")

    return score, issues, strengths


def _score_formatting(text: str) -> tuple[int, list[str], list[str]]:
    """Score formatting quality indicators (max 25 points)."""
    score = 0
    issues: list[str] = []
    strengths: list[str] = []

    word_count = len(text.split())

    # Length check: 300–1200 words is typical for a 1-2 page resume
    if 300 <= word_count <= 1500:
        score += 10
        strengths.append(f"Resume length ({word_count} words) is within optimal range")
    elif word_count < 150:
        issues.append(f"Resume is very short ({word_count} words) — ATS may flag as sparse")
    elif word_count > 1500:
        issues.append(f"Resume may be too long ({word_count} words) — consider trimming to 2 pages")

    # Bullet point detection (lines starting with - or •)
    bullet_lines = [
        l for l in text.splitlines()
        if l.strip().startswith(("-", "•", "*", "–"))
    ]
    if len(bullet_lines) >= 5:
        score += 10
        strengths.append("Uses bullet point formatting")
    else:
        issues.append("Limited use of bullet points — structured bullets improve ATS parsing")

    # No suspicious encoding or special characters
    special_chars = re.findall(r"[^\x00-\x7F]", text)
    if len(special_chars) < 20:
        score += 5
        strengths.append("Minimal special characters detected")
    else:
        issues.append("High number of non-ASCII characters may cause ATS parsing issues")

    return score, issues, strengths


def _score_dates(text: str) -> tuple[int, list[str], list[str]]:
    """Score date format consistency (max 15 points)."""
    score = 0
    issues: list[str] = []
    strengths: list[str] = []

    # Common date patterns: Jan 2023, 01/2023, 2020-2022, Present
    date_patterns = [
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\.?\s+\d{4}\b",
        r"\b\d{1,2}/\d{4}\b",
        r"\b\d{4}\s*[-–]\s*(?:\d{4}|Present|Current|Now)\b",
    ]
    found_dates = []
    for pattern in date_patterns:
        found_dates.extend(re.findall(pattern, text, re.IGNORECASE))

    if len(found_dates) >= 2:
        score += 15
        strengths.append("Work history dates detected in standard format")
    elif len(found_dates) == 1:
        score += 7
    else:
        issues.append("No work dates detected — ATS systems use dates to assess experience timeline")

    return score, issues, strengths


def compute_ats_score(text: str) -> ATSScoreResult:
    """Compute a holistic ATS-style compatibility score.

    Args:
        text: Full extracted resume text.

    Returns:
        ATSScoreResult with score, component breakdown, issues, and strengths.
    """
    contact_score, contact_issues, contact_strengths = _score_contact_info(text)
    section_score, section_issues, section_strengths = _score_sections(text)
    format_score, format_issues, format_strengths = _score_formatting(text)
    date_score, date_issues, date_strengths = _score_dates(text)

    total = contact_score + section_score + format_score + date_score

    return ATSScoreResult(
        score=min(total, 100),
        components={
            "contact_info": contact_score,
            "standard_sections": section_score,
            "formatting_quality": format_score,
            "date_consistency": date_score,
        },
        issues=contact_issues + section_issues + format_issues + date_issues,
        strengths=contact_strengths + section_strengths + format_strengths + date_strengths,
    )
