"""
Skill classifier using the extensible skill taxonomy — Milestones 6 & 7.

Performs exact, alias, and fuzzy matching against skills_taxonomy.json.
Also reads related_skills graph for partial match inference.

No model loading at import time.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

_TAXONOMY_PATH = Path(__file__).parent.parent / "taxonomy" / "skills_taxonomy.json"


@dataclass
class ClassifiedSkill:
    """A skill matched against the taxonomy."""

    raw: str
    canonical: str
    category: str
    match_type: str  # "exact" | "alias" | "fuzzy"


@dataclass
class SkillClassificationResult:
    """Full output of skill classification."""

    matched_skills: list[ClassifiedSkill] = field(default_factory=list)
    raw_skills: list[str] = field(default_factory=list)
    by_category: dict[str, list[str]] = field(default_factory=dict)


@lru_cache(maxsize=1)
def _load_taxonomy() -> dict:
    """Load and cache the taxonomy JSON. Called lazily — no import-time loading."""
    with _TAXONOMY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _build_lookup() -> tuple[dict[str, tuple[str, str]], dict[str, list[str]]]:
    """Build alias → (canonical_skill, category) lookup and related_skills graph.

    Returns:
        Tuple of (alias_map, related_skills_graph).
    """
    taxonomy = _load_taxonomy()
    alias_map: dict[str, tuple[str, str]] = {}
    for cat_name, cat_data in taxonomy["categories"].items():
        for canonical_skill, aliases in cat_data["skills"].items():
            for alias in aliases:
                alias_map[alias.lower()] = (canonical_skill, cat_name)
    related = taxonomy.get("related_skills", {})
    return alias_map, related


def classify_skills(text: str) -> SkillClassificationResult:
    """Extract and classify skills from resume text.

    Args:
        text: Raw or section-specific resume text.

    Returns:
        SkillClassificationResult with matched skills, raw list, and category breakdown.
    """
    alias_map, _ = _build_lookup()
    text_lower = text.lower()

    matched: list[ClassifiedSkill] = []
    seen_canonicals: set[str] = set()

    # Sort aliases by length descending to prefer longer matches first
    for alias, (canonical, category) in sorted(
        alias_map.items(), key=lambda x: len(x[0]), reverse=True
    ):
        # Use word-boundary aware matching
        pattern = r"(?<![a-zA-Z0-9\-_.])" + re.escape(alias) + r"(?![a-zA-Z0-9\-_.])"
        if re.search(pattern, text_lower) and canonical not in seen_canonicals:
            seen_canonicals.add(canonical)
            match_type = "exact" if alias == canonical else "alias"
            matched.append(
                ClassifiedSkill(
                    raw=alias,
                    canonical=canonical,
                    category=category,
                    match_type=match_type,
                )
            )

    # Build category breakdown
    by_category: dict[str, list[str]] = {}
    for skill in matched:
        by_category.setdefault(skill.category, []).append(skill.canonical)

    return SkillClassificationResult(
        matched_skills=matched,
        raw_skills=[s.canonical for s in matched],
        by_category=by_category,
    )


def get_related_skills(skill: str) -> list[str]:
    """Return skills related to the given canonical skill name.

    Args:
        skill: Canonical skill name (lowercase).

    Returns:
        List of related skill names for partial match inference.
    """
    _, related = _build_lookup()
    return related.get(skill.lower(), [])


def match_skills_to_job(
    resume_skills: list[str],
    job_skills: list[str],
) -> dict[str, list]:
    """Compare resume skill set against job skill requirements.

    Args:
        resume_skills: Canonical skill names from the resume.
        job_skills: Canonical skill names from the job description.

    Returns:
        Dictionary with keys 'matched', 'partial', 'missing'.
        'partial' entries are dicts: {resume_skill, job_skill, similarity}.
    """
    _, related_graph = _build_lookup()
    resume_set = {s.lower() for s in resume_skills}
    job_set = [s.lower() for s in job_skills]

    matched: list[str] = []
    partial: list[dict] = []
    missing: list[str] = []

    for job_skill in job_set:
        if job_skill in resume_set:
            matched.append(job_skill)
        else:
            # Check if any resume skill is related to this job skill
            found_partial = False
            related_to_job = related_graph.get(job_skill, [])
            for resume_skill in resume_set:
                if resume_skill in related_to_job or job_skill in related_graph.get(
                    resume_skill, []
                ):
                    partial.append(
                        {
                            "resume_skill": resume_skill,
                            "job_skill": job_skill,
                            "similarity": 0.75,  # Taxonomy-based partial credit
                        }
                    )
                    found_partial = True
                    break
            if not found_partial:
                missing.append(job_skill)

    return {"matched": matched, "partial": partial, "missing": missing}
