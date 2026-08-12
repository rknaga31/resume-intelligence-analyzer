"""
Resume section boundary detector — Milestone 5.

Classifies lines of a resume into named sections by normalising
common section header variations.

No model loading at import time.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class ResumeSection:
    """A detected section within a resume."""

    name: str
    canonical_name: str
    content: str
    start_line: int
    end_line: int


# Map of canonical section names to regex patterns matching common variations
_SECTION_PATTERNS: dict[str, list[str]] = {
    "Summary": [
        r"(?:professional\s+)?summary",
        r"(?:professional\s+)?profile",
        r"(?:career\s+)?objective",
        r"about\s+me",
        r"professional\s+background",
        r"executive\s+summary",
        r"overview",
    ],
    "Skills": [
        r"(?:technical\s+)?skills?",
        r"core\s+competencies",
        r"(?:key\s+)?competencies",
        r"technical\s+(?:expertise|stack|proficiencies?)",
        r"expertise",
        r"technologies",
        r"tools?\s+&?\s+technologies",
        r"programming\s+languages?",
    ],
    "Experience": [
        r"(?:work|professional|employment|career)\s+(?:experience|history|background)",
        r"experience",
        r"work\s+history",
        r"employment\s+(?:history|record)",
        r"professional\s+experience",
        r"relevant\s+experience",
    ],
    "Projects": [
        r"(?:major|key|notable|personal|academic|side)?\s*projects?",
        r"technical\s+projects?",
        r"portfolio",
        r"open[\s-]source\s+contributions?",
        r"software\s+projects?",
    ],
    "Education": [
        r"education(?:al\s+background)?",
        r"academic\s+(?:background|credentials|history|qualifications?)",
        r"degrees?",
        r"qualifications?",
        r"university\s+education",
    ],
    "Certifications": [
        r"certifications?(?:\s+&\s+licenses?)?",
        r"licenses?\s+(?:&\s+certifications?)?",
        r"professional\s+certifications?",
        r"credentials?",
        r"accreditations?",
    ],
    "Achievements": [
        r"achievements?",
        r"accomplishments?",
        r"honors?\s+&?\s+awards?",
        r"awards?(?:\s+&\s+honors?)?",
        r"recognitions?",
        r"accolades?",
    ],
    "Publications": [
        r"publications?",
        r"papers?",
        r"research(?:\s+publications?)?",
        r"journal\s+articles?",
    ],
    "Languages": [
        r"languages?",
        r"language\s+skills?",
        r"spoken\s+languages?",
    ],
    "Volunteering": [
        r"volunteer(?:ing)?(?:\s+experience)?",
        r"community\s+(?:service|involvement)",
        r"non[\s-]?profit\s+work",
    ],
    "Interests": [
        r"interests?",
        r"hobbies?",
        r"activities",
        r"extracurricular",
    ],
    "References": [
        r"references?",
        r"professional\s+references?",
    ],
}

# Build compiled regex patterns once at module level (not at import of models)
_COMPILED: dict[str, re.Pattern] = {}


def _build_patterns() -> None:
    """Compile all section header regex patterns."""
    for canonical, patterns in _SECTION_PATTERNS.items():
        combined = "|".join(f"(?:{p})" for p in patterns)
        _COMPILED[canonical] = re.compile(
            rf"^\s*(?:{combined})\s*:?\s*$",
            re.IGNORECASE | re.MULTILINE,
        )


_build_patterns()


def _is_section_header(line: str) -> str | None:
    """Return the canonical section name if this line is a header, else None.

    Args:
        line: A single line of resume text.

    Returns:
        Canonical section name string, or None if not a header.
    """
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return None
    for canonical, pattern in _COMPILED.items():
        if pattern.match(stripped):
            return canonical
    return None


def detect_sections(text: str) -> list[ResumeSection]:
    """Split resume text into named sections.

    Args:
        text: Full extracted resume text.

    Returns:
        Ordered list of ResumeSection objects.
    """
    lines = text.splitlines()
    sections: list[ResumeSection] = []
    current_section: str | None = None
    current_canonical: str | None = None
    current_start: int = 0
    buffer: list[str] = []

    def _flush(end_line: int) -> None:
        nonlocal current_section, current_canonical, buffer
        if current_canonical and buffer:
            sections.append(
                ResumeSection(
                    name=current_section or current_canonical,
                    canonical_name=current_canonical,
                    content="\n".join(buffer).strip(),
                    start_line=current_start,
                    end_line=end_line,
                )
            )
        elif buffer and not current_canonical:
            # Text before first section header → treat as Summary/header block
            sections.append(
                ResumeSection(
                    name="Header",
                    canonical_name="Header",
                    content="\n".join(buffer).strip(),
                    start_line=0,
                    end_line=end_line,
                )
            )
        buffer = []

    for i, line in enumerate(lines):
        detected = _is_section_header(line)
        if detected:
            _flush(i)
            current_section = line.strip()
            current_canonical = detected
            current_start = i
        else:
            buffer.append(line)

    _flush(len(lines))
    return sections


def get_section_names(text: str) -> list[str]:
    """Return a deduplicated list of canonical section names found in the text.

    Args:
        text: Full resume text.

    Returns:
        List of canonical section name strings.
    """
    seen: list[str] = []
    for sec in detect_sections(text):
        if sec.canonical_name not in seen:
            seen.append(sec.canonical_name)
    return seen
