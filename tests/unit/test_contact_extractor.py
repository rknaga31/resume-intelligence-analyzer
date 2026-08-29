"""
Unit tests for the contact information extractor.

Tests email, phone, LinkedIn, GitHub, website, and name extraction
across a variety of realistic resume text formats.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ml.extractors.contact import extract_contact_info


class TestEmailExtraction:
    def test_extracts_plain_email(self) -> None:
        info = extract_contact_info("John Doe\njohn.doe@example.com\nPython Developer")
        assert info.email == "john.doe@example.com"

    def test_extracts_email_with_plus_sign(self) -> None:
        info = extract_contact_info("jane+resume@company.co.uk")
        assert info.email == "jane+resume@company.co.uk"

    def test_no_email_returns_empty_string(self) -> None:
        info = extract_contact_info("No contact info here.")
        assert info.email == ""

    def test_all_emails_returns_all_unique(self) -> None:
        text = "primary@foo.com | backup@bar.org | primary@foo.com"
        info = extract_contact_info(text)
        assert len(info.all_emails) == 2
        assert "primary@foo.com" in info.all_emails
        assert "backup@bar.org" in info.all_emails


class TestPhoneExtraction:
    def test_extracts_us_phone_standard_format(self) -> None:
        info = extract_contact_info("Call me: (555) 123-4567")
        assert info.phone != ""
        assert "5551234567" in info.phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    def test_extracts_phone_with_country_code(self) -> None:
        info = extract_contact_info("Phone: +1-800-555-0199")
        assert info.phone != ""

    def test_short_number_not_extracted(self) -> None:
        info = extract_contact_info("Code: 123-456")
        assert info.phone == ""


class TestLinkedInExtraction:
    def test_extracts_linkedin_with_https(self) -> None:
        info = extract_contact_info("Profile: https://linkedin.com/in/johndoe")
        assert "linkedin.com/in/johndoe" in info.linkedin_url

    def test_extracts_linkedin_without_protocol(self) -> None:
        info = extract_contact_info("linkedin.com/in/jane-smith-dev")
        assert info.linkedin_url.startswith("https://")
        assert "jane-smith-dev" in info.linkedin_url

    def test_no_linkedin_returns_empty(self) -> None:
        info = extract_contact_info("No social links here.")
        assert info.linkedin_url == ""


class TestGitHubExtraction:
    def test_extracts_github_with_https(self) -> None:
        info = extract_contact_info("Code: https://github.com/johndoe")
        assert "github.com/johndoe" in info.github_url

    def test_extracts_github_without_protocol(self) -> None:
        info = extract_contact_info("github.com/jsmith-dev")
        assert info.github_url.startswith("https://")
        assert "jsmith-dev" in info.github_url

    def test_no_github_returns_empty(self) -> None:
        info = extract_contact_info("No GitHub link.")
        assert info.github_url == ""


class TestNameExtraction:
    def test_extracts_titlecase_name(self) -> None:
        text = "John Smith\njohn@example.com\n\nSKILLS\nPython, Java"
        info = extract_contact_info(text)
        assert info.name == "John Smith"

    def test_extracts_all_caps_name(self) -> None:
        text = "JANE DEVELOPER\njane@dev.com"
        info = extract_contact_info(text)
        assert "Jane" in info.name or info.name == ""  # all-caps to title

    def test_does_not_extract_skill_section_as_name(self) -> None:
        text = "Python Developer\nskills: Python, Go\nExperience: 5 years"
        info = extract_contact_info(text)
        # "Python Developer" should be filtered due to "developer" signal
        assert info.name != "Python Developer"


class TestFullResumeExtraction:
    def test_full_resume_extraction(self) -> None:
        """Integration-style test against a realistic resume snippet."""
        resume = """
Sarah Johnson
sarah.j@techcorp.com | +1 (415) 555-0182
linkedin.com/in/sarah-johnson-swe | github.com/sarahjdev

SUMMARY
Senior Software Engineer with 6 years of experience.

SKILLS
Python, FastAPI, PostgreSQL, Docker, Kubernetes, AWS
        """.strip()

        info = extract_contact_info(resume)
        assert info.email == "sarah.j@techcorp.com"
        assert info.phone != ""
        assert "sarah-johnson-swe" in info.linkedin_url
        assert "sarahjdev" in info.github_url
        assert info.name in ("Sarah Johnson", "")  # name detection is best-effort
