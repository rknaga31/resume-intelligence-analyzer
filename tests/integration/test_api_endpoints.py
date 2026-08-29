"""Integration tests for FastAPI REST API endpoints.

Tests health check, resume file upload, validation, and full analysis endpoints.
"""

from __future__ import annotations

import io

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check_endpoint():
    """Test GET /api/v1/health returns 200 OK with expected status and version."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
    assert "environment" in data


def test_upload_resume_txt_success():
    """Test POST /api/v1/resumes/upload with valid TXT file."""
    content = b"John Doe\nSoftware Engineer\nSkills: Python, FastAPI, Docker, PostgreSQL\nExperience: Built REST APIs."
    files = {"file": ("resume.txt", io.BytesIO(content), "text/plain")}

    response = client.post("/api/v1/resumes/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["filename"] == "resume.txt"
    assert data["mime_type"] == "text/plain"
    assert "Python, FastAPI" in data["extracted_text"]
    assert data["word_count"] > 0


def test_upload_resume_unsupported_filetype():
    """Test POST /api/v1/resumes/upload with invalid file extension/MIME."""
    content = b"\x00\x01\x02\x03\x04"
    files = {"file": ("malicious.exe", io.BytesIO(content), "application/x-msdownload")}

    response = client.post("/api/v1/resumes/upload", files=files)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "UNSUPPORTED_FILE_TYPE"


def test_full_analysis_endpoint_success():
    """Test POST /api/v1/analyze/full with valid payload."""
    payload = {
        "resume_text": """
        Jane Developer
        Senior Backend Engineer

        EXPERIENCE
        Senior Engineer | TechCorp | 2021 - Present
        • Architected microservices with Python, FastAPI, and PostgreSQL handling 5M req/day, improving latency by 35%.
        • Deployed Docker containers on Kubernetes with AWS ECS.

        SKILLS
        Python, FastAPI, Docker, Kubernetes, PostgreSQL, AWS, Redis, Git, CI/CD
        """,
        "target_role": "Senior Python Backend Engineer",
        "job_description": "We are seeking a Senior Backend Engineer with expertise in Python, FastAPI, Docker, Kubernetes, and PostgreSQL.",
    }

    response = client.post("/api/v1/analyze/full", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "analysis_id" in data
    assert data["target_role"] == "Senior Python Backend Engineer"

    # Scores
    scores = data["scores"]
    assert 0 <= scores["overall_score"] <= 100
    assert 0 <= scores["ats_compatibility_score"] <= 100
    assert 0 <= scores["job_match_score"] <= 100

    # Skills
    skills = data["skills"]
    assert isinstance(skills["matched"], list)
    assert len(skills["resume_skills"]) > 0

    # LLM synthesis
    synthesis = data["llm_synthesis"]
    assert len(synthesis["executive_summary"]) > 0
    assert len(synthesis["strengths"]) > 0
    assert len(synthesis["actionable_recommendations"]) > 0


def test_full_analysis_validation_error():
    """Test POST /api/v1/analyze/full with missing required fields."""
    payload = {
        "resume_text": "Short",  # Too short (min 20 chars)
        "target_role": "",  # Empty target role
    }

    response = client.post("/api/v1/analyze/full", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (Pydantic validation error)
