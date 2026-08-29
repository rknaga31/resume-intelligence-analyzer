"""
Contact information extractor — regex-based NER.

Extracts email, phone, LinkedIn URL, GitHub URL, website, and candidate
name from raw resume text. No spaCy model loading at import time.

All patterns are compiled once at module level for performance.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Compiled patterns
# ---------------------------------------------------------------------------

_EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
)

_PHONE_RE = re.compile(
    r"(?:\+?1[\s\-.]?)?"                          # optional +1 country code
    r"(?:\(?\d{3}\)?[\s\-.]?)?"                   # optional area code
    r"\d{3}[\s\-.]?\d{4}"                         # 7-digit local number
    r"(?:\s?(?:x|ext)\.?\s?\d{1,5})?",            # optional extension
)

_LINKEDIN_RE = re.compile(
    r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w\-]+/?",
    re.IGNORECASE,
)

_GITHUB_RE = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/[\w\-]+(?:/[\w\-]+)?/?",
    re.IGNORECASE,
)

_WEBSITE_RE = re.compile(
    r"https?://(?!(?:www\.)?(?:linkedin|github)\.com)[^\s,<>\"']+",
    re.IGNORECASE,
)

# Patterns that strongly suggest a line is NOT a person's name
_NON_NAME_SIGNALS = re.compile(
    r"[\|@\d/\\]|resume|cv|curriculum|vitae|objective|summary|experience|"
    r"education|skills|profile|engineer|developer|analyst|manager|director",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Output dataclass
# ---------------------------------------------------------------------------

@dataclass
class ContactInfo:
    """Extracted contact information from a resume.

    Attributes:
        name: Best-guess candidate name (first non-empty line heuristic).
        email: Primary email address or empty string.
        phone: Primary phone number or empty string.
        linkedin_url: LinkedIn profile URL or empty string.
        github_url: GitHub profile URL or empty string.
        website: Personal website URL or empty string.
        all_emails: All email addresses found in the document.
        all_phones: All phone numbers found in the document.
    """

    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin_url: str = ""
    github_url: str = ""
    website: str = ""
    all_emails: list[str] = field(default_factory=list)
    all_phones: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------

def extract_contact_info(text: str) -> ContactInfo:
    """Extract contact information from resume text.

    Args:
        text: Raw resume text (plain text, not HTML).

    Returns:
        ContactInfo dataclass with all extracted fields.
    """
    info = ContactInfo()

    # --- Email ---
    emails = [m.group() for m in _EMAIL_RE.finditer(text)]
    info.all_emails = _deduplicate(emails)
    if info.all_emails:
        info.email = info.all_emails[0]

    # --- Phone ---
    phones = [_normalise_phone(m.group()) for m in _PHONE_RE.finditer(text)]
    phones = [p for p in phones if len(re.sub(r"\D", "", p)) >= 7]
    info.all_phones = _deduplicate(phones)
    if info.all_phones:
        info.phone = info.all_phones[0]

    # --- LinkedIn ---
    m = _LINKEDIN_RE.search(text)
    if m:
        url = m.group()
        info.linkedin_url = url if url.startswith("http") else f"https://{url}"

    # --- GitHub ---
    m = _GITHUB_RE.search(text)
    if m:
        url = m.group()
        info.github_url = url if url.startswith("http") else f"https://{url}"

    # --- Website ---
    m = _WEBSITE_RE.search(text)
    if m:
        info.website = m.group().rstrip(".,;)")

    # --- Name (first non-empty, non-contact-looking line heuristic) ---
    for line in text.splitlines():
        line = line.strip()
        if (
            line
            and 2 <= len(line.split()) <= 5
            and not _NON_NAME_SIGNALS.search(line)
            and not _EMAIL_RE.search(line)
            and not _PHONE_RE.search(line)
            and not _LINKEDIN_RE.search(line)
        ):
            # Accept title-case or ALL-CAPS lines as likely name candidates
            if line.istitle() or line.isupper():
                info.name = line.title()
                break
            # Also accept mixed-case lines that look like names
            if all(word[0].isupper() for word in line.split() if word):
                info.name = line
                break

    return info


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _deduplicate(items: list[str]) -> list[str]:
    """Return deduplicated list preserving order."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _normalise_phone(raw: str) -> str:
    """Trim whitespace from a raw phone match."""
    return raw.strip()
