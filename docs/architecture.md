# Architectural Specification — Resume Intelligence Analyzer

## 1. System Overview

The **Resume Intelligence Analyzer** is designed as a decoupled, multi-tiered AI/ML web application. It transforms raw candidate resume documents into structured, explainable career intelligence using a hybrid engine that combines rule-based document parsing, deterministic NLP entity recognition, transformer vector embeddings, explainable scoring algorithms, and structured LLM reasoning with strict prompt-injection defenses.

---

## 2. High-Level Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                                       USER AGENT                                         │
│                              Browser (React 18 / Next.js 14+)                            │
└──────────────────────────────────────────┬───────────────────────────────────────────────┘
                                           │ HTTPS / JSON API v1
┌──────────────────────────────────────────▼───────────────────────────────────────────────┐
│                                    API GATEWAY LAYER                                     │
│                     FastAPI Async Server (Uvicorn / Python 3.13)                         │
│               - Middleware (CORS, Rate Limiting, Request ID, Error Handling)            │
│               - Request Validation (Pydantic v2 schemas)                                │
└──────────────────────┬──────────────────────────────────────────┬────────────────────────┘
                       │                                          │
┌──────────────────────▼─────────────────────┐  ┌─────────────────▼────────────────────────┐
│     DOCUMENT PROCESSING PIPELINE           │  │     JOB DESCRIPTION INTELLIGENCE         │
│  - MIME & Magic Byte Validation            │  │  - Requirement Categorization            │
│  - PDF/DOCX/TXT Sanitized Extraction       │  │    (Required / Preferred / Optional)     │
│  - Traversal & Empty File Guard            │  │  - Tech Stack & Responsibilities Parser │
└──────────────────────┬─────────────────────┘  └─────────────────┬────────────────────────┘
                       │                                          │
┌──────────────────────▼──────────────────────────────────────────▼────────────────────────┐
│                                RESUME INTELLIGENCE ENGINE                                │
│  - Section Classifier (Summary, Skills, Experience, Education, Projects, Certs)          │
│  - Named Entity Recognition (Contact Info, Dates, Institutions, Titles, Metrics)         │
│  - Skill Taxonomy Classifier (15+ Technical & Soft Skill Categories)                    │
└──────────────────────┬───────────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────────────────────────────────┐
│                              SEMANTIC MATCHING & EMBEDDINGS                              │
│  - SentenceTransformers (`all-MiniLM-L6-v2`) Embedding Encoder                            │
│  - Section & Skill Cosine Similarity Vector Calculation                                  │
│  - Partial & Related Skill Graph Mapping (e.g. PyTorch ↔ TensorFlow)                      │
└──────────────────────┬───────────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────────────────────────────────┐
│                          EXPLAINABLE SCORING & IMPACT ANALYZER                           │
│  - ATS-Style Compatibility Analyzer (Formatting, Standard Sections, Contact completeness)│
│  - Achievement Impact Auditor (Quantified metrics %, $, scale, latency, accuracy)       │
│  - Multi-Dimensional Weighted Scoring Matrix                                             │
└──────────────────────┬───────────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────────────────────────────────┐
│                            LLM REASONING & PROMPT INJECTION GUARD                        │
│  - Untrusted Content Isolation (<untrusted_document_content> sandbox)                   │
│  - Multi-Provider Adapter (OpenAI / Anthropic / Gemini / Local Fallback)                  │
│  - Structured Pydantic Output Validation & Retry Handler                                 │
└──────────────────────┬───────────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────────────────────────────────┐
│                             PERSISTENCE & AUDIT LOG STORE                                │
│  - PostgreSQL (SQLAlchemy 2.0 Async Session)                                             │
│  - Temporary Upload Storage (Auto-Purged Post Processing)                                │
│  - Zero PII Technical Audit Logging                                                      │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow Specification

1. **Upload & Ingestion**:
   - Client sends document binary via `POST /api/v1/resumes/upload`.
   - Backend validates magic bytes (`%PDF-`, `PK\x03\x04`) and file size limits.
   - Text is extracted into memory via multi-backend fallback (`pypdf` → `pdfplumber` → `python-docx`).
   - Disk temporary files are purged immediately.

2. **Parsing & Entity Extraction**:
   - `ml/parsers/section_detector.py` segments document into sections based on normalized headers.
   - `ml/extractors/contact.py` isolates PII (Name, Email, Phone, Social links).
   - `ml/extractors/skill_classifier.py` maps skills against taxonomy across 15 categories.

3. **Job Analysis & Semantic Matching**:
   - Job description is parsed into Required, Preferred, and Optional criteria.
   - `SentenceTransformers` encodes text into 384-dimensional dense vectors.
   - Cosine similarity is computed between Resume sections and Job criteria.
   - Skill coverage graph identifies Matched, Related (partial credit), and Missing skills.

4. **Scoring & LLM Synthesis**:
   - Scoring engine computes ATS-Style Score, Job Match Score, Achievement Score, and Resume Quality.
   - LLM receives structured JSON payload with untrusted text enclosed in security tags.
   - LLM generates bullet point improvements, strengths, weaknesses, and a career roadmap.
   - Output validated against Pydantic response models before returning to client.

---

## 4. Architectural Principles & Constraints

- **Decoupled Engine**: The ML/NLP pipeline can be run headlessly without web dependencies.
- **Explainability First**: Every numerical score includes evidence strings and human-readable reasoning.
- **Fail-Safe Operation**: If external LLM APIs fail or timing out, system falls back to rule-based analysis without breaking user experience.
- **Zero-PII Storage**: Candidate document text is processed transiently and deleted after analysis.
