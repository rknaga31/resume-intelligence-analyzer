"""
Contact information extractor — Milestone 4.

Extracts: name, email, phone, location, LinkedIn, GitHub, portfolio URLs.

SECURITY: Extracted PII is NEVER written to logs. Only technical metadata is logged.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Compiled Regex Patterns
# ---------------------------------------------------------------------------

_EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
)

_PHONE_RE = re.compile(
    r"(?:\+?\d[\d\s\-().]{7,}\d)"
)

_LINKEDIN_RE = re.compile(
    r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w\-]+"
    r"|linkedin\.com/in/[\w\-]+",
    re.IGNORECASE,
)

_GITHUB_RE = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/[\w\-]+"
    r"|github\.com/[\w\-]+",
    re.IGNORECASE,
)

_URL_RE = re.compile(
    r"https?://[^\s\"'<>]{4,}",
    re.IGNORECASE,
)

# Simple location heuristic: "City, ST" or "City, Country"
_LOCATION_RE = re.compile(
    r"\b([A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,})*),\s*([A-Z]{2}|[A-Z][a-z]{3,})\b"
)


def extract_contact_info(text: str) -> dict[str, str | None]:
    """Extract contact fields from raw resume text.

    Args:
        text: Full resume text.

    Returns:
        Dictionary with keys: name, email, phone, location, linkedin, github, portfolio.
        Missing fields are None.
    """
    email = _extract_email(text)
    phone = _extract_phone(text)
    linkedin = _extract_linkedin(text)
    github = _extract_github(text)
    portfolio = _extract_portfolio(text, exclude={linkedin, github})
    name = _extract_name(text)
    location = _extract_location(text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio,
    }


def _extract_email(text: str) -> str | None:
    """Extract first email address found."""
    match = _EMAIL_RE.search(text)
    return match.group(0) if match else None


def _extract_phone(text: str) -> str | None:
    """Extract first phone number found (7-15 digits with formatting)."""
    match = _PHONE_RE.search(text)
    if match:
        raw = match.group(0).strip()
        # Filter out numbers that are too short or too long
        digits = re.sub(r"\D", "", raw)
        if 7 <= len(digits) <= 15:
            return raw
    return None


def _extract_linkedin(text: str) -> str | None:
    """Extract LinkedIn profile URL."""
    match = _LINKEDIN_RE.search(text)
    return match.group(0).rstrip("/") if match else None


def _extract_github(text: str) -> str | None:
    """Extract GitHub profile URL."""
    match = _GITHUB_RE.search(text)
    if match:
        url = match.group(0).rstrip("/")
        # Exclude GitHub Actions / raw content URLs
        if "/actions" not in url and "githubusercontent" not in url:
            return url
    return None


def _extract_portfolio(text: str, exclude: set[str | None]) -> str | None:
    """Extract portfolio/personal website URL (excluding LinkedIn and GitHub)."""
    for match in _URL_RE.finditer(text):
        url = match.group(0).rstrip("/.,;)")
        if url not in exclude and "linkedin.com" not in url and "github.com" not in url:
            return url
    return None


def _extract_name(text: str) -> str | None:
    """Heuristically extract candidate name from the first few lines.

    The name is typically the first non-empty line that is not an email,
    phone, or URL, and looks like a proper name (2-4 words, title-cased).
    """
    for line in text.splitlines()[:10]:
        stripped = line.strip()
        if not stripped:
            continue
        # Skip lines that look like contact info
        if _EMAIL_RE.search(stripped):
            continue
        if _PHONE_RE.search(stripped):
            continue
        if _URL_RE.search(stripped):
            continue
        # Must be 1-4 words, mostly alphabetic
        words = stripped.split()
        if 1 <= len(words) <= 5 and all(
            re.match(r"^[A-Za-z\-'.]{1,30}$", w) for w in words
        ):
            return stripped
    return None


def _extract_location(text: str) -> str | None:
    """Extract city/state or city/country location string."""
    match = _LOCATION_RE.search(text[:500])  # Location usually near the top
    return match.group(0) if match else None
