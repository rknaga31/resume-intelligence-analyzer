"""
Achievement Impact Analyzer — Milestone 9.

Analyzes experience bullet points for quantifiable impact evidence:
percentages, numbers, scales, financial figures, latency, accuracy.

IMPORTANT: The system NEVER invents metrics.
If a bullet lacks quantification, it recommends HOW to add metrics
without fabricating specific numbers.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class BulletAnalysis:
    """Analysis of a single experience bullet point."""

    text: str
    is_quantified: bool
    metrics_found: list[str] = field(default_factory=list)
    issue: str | None = None
    suggestion: str | None = None


@dataclass
class AchievementAnalysisResult:
    """Aggregate achievement impact analysis."""

    quantified_count: int
    total_count: int
    quantification_rate: float
    score: int
    bullets: list[BulletAnalysis] = field(default_factory=list)


# Patterns that indicate quantified impact
_QUANTIFICATION_PATTERNS = [
    (r"\b\d+(?:\.\d+)?%", "percentage"),
    (r"\$\s*\d+(?:[,.\d]+)?(?:\s*[KMBkmb](?:illion|illion|illion)?)?", "financial figure"),
    (r"\b\d+(?:[,.\d]+)?\s*(?:K|M|B|k|m|b|million|billion|thousand)\b", "scale metric"),
    (r"\b(?:reduced|improved|increased|decreased|optimized|saved|generated|processed|scaled|grew)\b.*\d+", "impact verb + number"),
    (r"\b\d+(?:ms|seconds?|minutes?|hours?)\b", "latency/time"),
    (r"\b\d+(?:[,.\d]+)?\s*(?:users?|customers?|clients?|requests?|transactions?|records?)\b", "user/volume scale"),
    (r"\b(?:accuracy|precision|recall|f1|auc|latency|throughput|uptime)\s*(?:of\s*)?\d+(?:\.\d+)?%?", "ML/performance metric"),
    (r"\b(?:first|fastest|largest|highest|lowest)\b", "superlative achievement"),
]

_COMPILED_PATTERNS = [
    (re.compile(pattern, re.IGNORECASE), label)
    for pattern, label in _QUANTIFICATION_PATTERNS
]

# Improvement suggestion templates per weakness type
_SUGGESTIONS = {
    "no_action_verb": (
        "Start with a strong action verb (e.g., 'Developed', 'Architected', 'Optimized', 'Led') "
        "to make the bullet more impactful."
    ),
    "no_metric": (
        "Add a measurable outcome — e.g., scale (10K users), performance gain (40% faster), "
        "time saved (reduced processing time by 2 hours), or business impact ($50K cost reduction). "
        "Use your actual numbers — do not invent figures."
    ),
    "too_vague": (
        "Make the action more specific: what exactly did you build or change? "
        "What was the before/after state? What technology was used?"
    ),
}

_ACTION_VERB_RE = re.compile(
    r"^(?:developed|built|designed|implemented|created|architected|led|managed|improved|"
    r"optimized|deployed|launched|automated|scaled|migrated|reduced|increased|trained|"
    r"engineered|established|mentored|defined|delivered|integrated|owned|drove|transformed|"
    r"analyzed|researched|investigated|collaborated)\b",
    re.IGNORECASE,
)


def _analyze_bullet(text: str) -> BulletAnalysis:
    """Analyze a single bullet point for quantification and quality.

    Args:
        text: A single experience bullet point.

    Returns:
        BulletAnalysis with metrics found, issue description, and improvement suggestion.
    """
    metrics: list[str] = []
    for pattern, label in _COMPILED_PATTERNS:
        if pattern.search(text):
            metrics.append(label)

    is_quantified = len(metrics) > 0

    issue: str | None = None
    suggestion: str | None = None

    if not is_quantified:
        if not _ACTION_VERB_RE.match(text.strip()):
            issue = "Bullet lacks a strong action verb and measurable outcome"
            suggestion = (
                f"{_SUGGESTIONS['no_action_verb']} "
                f"{_SUGGESTIONS['no_metric']}"
            )
        elif len(text.split()) < 8:
            issue = "Bullet is too vague and brief"
            suggestion = _SUGGESTIONS["too_vague"]
        else:
            issue = "Bullet lacks a measurable outcome or quantifiable metric"
            suggestion = _SUGGESTIONS["no_metric"]

    return BulletAnalysis(
        text=text,
        is_quantified=is_quantified,
        metrics_found=metrics,
        issue=issue,
        suggestion=suggestion,
    )


def _extract_bullets(text: str) -> list[str]:
    """Extract experience bullet points from text."""
    bullets = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "•", "–", "*")) and len(stripped) > 15:
            bullet_text = stripped.lstrip("-•–* ").strip()
            if bullet_text:
                bullets.append(bullet_text)
    return bullets


def analyze_achievements(text: str) -> AchievementAnalysisResult:
    """Analyze all experience bullets in the resume for quantified impact.

    Args:
        text: Full resume text or experience section text.

    Returns:
        AchievementAnalysisResult with bullet-level and aggregate analysis.
    """
    bullets = _extract_bullets(text)

    if not bullets:
        return AchievementAnalysisResult(
            quantified_count=0,
            total_count=0,
            quantification_rate=0.0,
            score=0,
            bullets=[],
        )

    analyses = [_analyze_bullet(b) for b in bullets]
    quantified = sum(1 for a in analyses if a.is_quantified)
    rate = quantified / len(analyses) if analyses else 0.0

    # Score based on quantification rate
    if rate >= 0.70:
        score = 90 + int((rate - 0.70) * 33)  # 90-100
    elif rate >= 0.50:
        score = 75 + int((rate - 0.50) * 75)  # 75-90
    elif rate >= 0.25:
        score = 50 + int((rate - 0.25) * 100)  # 50-75
    else:
        score = int(rate * 200)  # 0-50

    return AchievementAnalysisResult(
        quantified_count=quantified,
        total_count=len(analyses),
        quantification_rate=round(rate, 2),
        score=min(score, 100),
        bullets=analyses,
    )
