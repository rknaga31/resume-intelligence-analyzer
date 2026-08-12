# API Specification — Resume Intelligence Analyzer (v1)

## 1. Base URL & OpenAPI

- **Base URL**: `http://localhost:8000/api/v1`
- **Swagger Documentation**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 2. Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | System health check and runtime metrics |
| `POST` | `/resumes/upload` | Upload and extract raw text from PDF/DOCX |
| `POST` | `/resumes/parse` | Parse resume into structured JSON entities |
| `POST` | `/jobs/analyze` | Parse job description into skill/role requirements |
| `POST` | `/analyze/match` | Perform semantic match between resume & job description |
| `POST` | `/analyze/full` | Complete end-to-end intelligence analysis & LLM synthesis |

---

## 3. Detailed Request/Response Schemas

### `GET /api/v1/health`
**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "timestamp": "2026-08-12T23:30:00Z",
  "services": {
    "database": "connected",
    "redis": "connected",
    "ml_engine": "ready"
  }
}
```

### `POST /api/v1/resumes/upload`
**Content-Type**: `multipart/form-data`
**Parameters**:
- `file`: Resume file (PDF, DOCX, TXT; max 10MB)

**Response (200 OK):**
```json
{
  "file_id": "res_8f921a4e",
  "filename": "candidate_resume.pdf",
  "file_size": 412950,
  "mime_type": "application/pdf",
  "extracted_text": "Jane Doe\nSenior AI Engineer...",
  "word_count": 640,
  "character_count": 4120
}
```

**Errors**:
- `400 Bad Request`: File type not supported or corrupted file.
- `413 Payload Too Large`: File size exceeds `MAX_UPLOAD_SIZE_MB`.

### `POST /api/v1/analyze/full`
**Request (JSON):**
```json
{
  "resume_text": "Jane Doe...",
  "target_role": "Senior AI / Machine Learning Engineer",
  "job_description": "We are seeking a Senior AI Engineer proficient in Python, PyTorch, FastAPI, and Docker..."
}
```

**Response (200 OK):**
```json
{
  "analysis_id": "an_99c301bd",
  "timestamp": "2026-08-12T23:31:00Z",
  "scores": {
    "overall_score": 88,
    "ats_compatibility_score": 92,
    "job_match_score": 85,
    "achievement_impact_score": 80,
    "skill_relevance_score": 90
  },
  "contact_info": {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "phone": "+1-555-0199",
    "location": "San Francisco, CA",
    "linkedin": "https://linkedin.com/in/janedoe",
    "github": "https://github.com/janedoe"
  },
  "skills": {
    "matched": ["Python", "FastAPI", "Docker", "NLP"],
    "partial": [
      {"resume_skill": "TensorFlow", "job_skill": "PyTorch", "similarity": 0.85}
    ],
    "missing": ["AWS", "Kubernetes"]
  },
  "sections_found": ["Summary", "Skills", "Experience", "Projects", "Education"],
  "achievement_analysis": {
    "quantified_bullets_count": 4,
    "total_bullets_count": 6,
    "quantification_rate": 0.67,
    "bullet_feedback": [
      {
        "original": "Built ML pipeline.",
        "issue": "Lacks measurable outcome or scale metric.",
        "suggestion": "Built ML pipeline processing 50K daily requests with 99.2% uptime."
      }
    ]
  },
  "llm_synthesis": {
    "executive_summary": "Strong candidate with solid ML engineering background.",
    "strengths": ["Clear technical stack", "Quantified achievements in prior role"],
    "weaknesses": ["Missing cloud infrastructure evidence (AWS)"],
    "actionable_recommendations": [
      "Add evidence of AWS or GCP cloud deployment in project bullets."
    ],
    "career_roadmap": [
      "Step 1: Obtain AWS Certified Machine Learning Specialist",
      "Step 2: Add Kubernetes deployment evidence to project section"
    ]
  }
}
```

---

## 4. Error Handling Standard

All API errors return RFC 7807 compliant JSON:
```json
{
  "error": {
    "code": "INVALID_FILE_FORMAT",
    "message": "The provided file header '%PNG' does not match supported resume document types (PDF, DOCX, TXT).",
    "details": null,
    "request_id": "req_5510ab2c"
  }
}
```
