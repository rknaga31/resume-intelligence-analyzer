# Resume Intelligence Analyzer

> **Status: 🚧 In Development — initial repository scaffolding**

An AI-powered platform that transforms resumes into structured intelligence, enabling deep analysis, semantic matching, and actionable career insights using large language models and modern NLP techniques.

---

## Table of Contents

- [Overview](#overview)
- [Planned Features](#planned-features)
- [Planned Architecture](#planned-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Development Roadmap](#development-roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Resume Intelligence Analyzer** is a full-stack AI/ML application designed to:

- Parse and extract structured information from resumes in multiple formats (PDF, DOCX, TXT)
- Apply NLP and LLM-based analysis to surface skills, experience timelines, and career trajectories
- Perform semantic job-description matching using vector embeddings
- Provide recruiters and candidates with actionable insights and gap analysis
- Expose a clean REST API for integration with external ATS and HR systems

This project is in its **initial scaffolding phase**. No application features are implemented yet.

---

## Planned Features

### Core Analysis
- [ ] Multi-format resume parsing (PDF, DOCX, TXT)
- [ ] Named entity extraction (skills, roles, companies, education, certifications)
- [ ] Experience timeline reconstruction and career gap detection
- [ ] Skill taxonomy mapping and normalization
- [ ] Semantic similarity scoring between resume and job description

### AI / LLM Capabilities
- [ ] LLM-powered resume summarization
- [ ] Intelligent feedback and improvement suggestions
- [ ] Multi-LLM support (OpenAI GPT-4o, Anthropic Claude, Google Gemini)
- [ ] RAG (Retrieval-Augmented Generation) for context-aware analysis
- [ ] Vector embedding search for candidate ranking

### Platform
- [ ] Secure file upload and temporary storage
- [ ] User authentication and authorization (JWT)
- [ ] Dashboard for recruiters with batch-analysis support
- [ ] REST API with OpenAPI / Swagger documentation
- [ ] Export results as JSON, PDF reports, or CSV

### Infrastructure
- [ ] Docker Compose development environment
- [ ] GitHub Actions CI/CD pipeline
- [ ] Automated testing (unit, integration, E2E)
- [ ] Monitoring and observability

---

## Planned Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│              React / Next.js + TypeScript Frontend           │
│                  (Upload UI · Dashboard · Reports)           │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTPS / REST
┌────────────────────────▼─────────────────────────────────────┐
│                     API Gateway Layer                        │
│                FastAPI (Python) — Async REST API             │
│              Auth · Validation · Rate Limiting               │
└──────────┬─────────────────────────────┬────────────────────-┘
           │                             │
┌──────────▼──────────┐   ┌─────────────▼──────────────────────┐
│   ML / NLP Engine   │   │         Data Layer                 │
│  Parsing · NER      │   │  PostgreSQL (structured data)       │
│  Embeddings · LLMs  │   │  Vector DB (semantic search)        │
│  Scoring · RAG      │   │  Redis (cache · task queue)         │
└─────────────────────┘   └────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18, Next.js 14+, TypeScript, Tailwind CSS |
| **Backend API** | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0 |
| **Database** | PostgreSQL 15+ (primary), Redis (cache/queue) |
| **ML / NLP** | spaCy, Transformers (HuggingFace), LangChain |
| **LLMs** | OpenAI GPT-4o, Anthropic Claude, Google Gemini |
| **Vector DB** | Pinecone / Qdrant / Weaviate (TBD) |
| **Document Parsing** | pdfplumber, python-docx, PyMuPDF |
| **Auth** | JWT (python-jose), bcrypt |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Testing** | pytest, pytest-asyncio, Playwright (E2E) |
| **Monitoring** | Sentry, LangSmith (LLM tracing) |

---

## Project Structure

```
resume-intelligence-analyzer/
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── api/            # Route handlers
│   │   ├── core/           # Config, security, logging
│   │   ├── db/             # Models, migrations, session
│   │   ├── schemas/        # Pydantic request/response models
│   │   └── services/       # Business logic layer
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React / Next.js application
│   ├── src/
│   │   ├── app/            # Next.js app router pages
│   │   ├── components/     # Reusable UI components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── lib/            # API client, utilities
│   │   └── types/          # TypeScript type definitions
│   ├── package.json
│   └── Dockerfile
├── ml/                     # ML & NLP pipeline
│   ├── parsers/            # Document parsing modules
│   ├── extractors/         # NER and entity extraction
│   ├── embeddings/         # Vector embedding pipeline
│   ├── llm/                # LLM integration wrappers
│   └── scoring/            # Matching and scoring logic
├── tests/                  # Test suites
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/                   # Project documentation
│   ├── architecture/
│   ├── api/
│   └── guides/
├── scripts/                # Dev & ops utility scripts
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
├── .env.example            # Environment variable template
├── .gitignore
├── docker-compose.yml      # Local development services
├── AGENTS.md               # AI agent instructions
├── LICENSE
└── README.md
```

---

## Getting Started

> ⚠️ **Application code has not been implemented yet.** The following steps will be valid once development begins.

### Prerequisites

- Python 3.11+
- Node.js 20+ and npm / pnpm
- Docker Desktop
- Git

### Setup (upcoming)

```bash
# 1. Clone the repository
git clone https://github.com/rknaga31/resume-intelligence-analyzer.git
cd resume-intelligence-analyzer

# 2. Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys and database credentials

# 3. Start infrastructure services
docker compose up -d postgres redis

# 4. Set up Python backend
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 5. Set up Node frontend
cd ../frontend
npm install

# 6. Start development servers
# Terminal 1 — backend
cd backend && uvicorn app.main:app --reload

# Terminal 2 — frontend
cd frontend && npm run dev
```

---

## Environment Variables

Copy `.env.example` to `.env` and populate the values. See [`.env.example`](.env.example) for the full reference.

**Required to run:**
- `POSTGRES_*` — database connection
- `OPENAI_API_KEY` (or another LLM provider key)
- `APP_SECRET_KEY` and `JWT_SECRET_KEY`

---

## Development Roadmap

| Phase | Description | Status |
|---|---|---|
| **0 — Repository Setup** | Scaffold project, CI/CD, documentation | 🚧 In Progress |
| **1 — Core Infrastructure** | FastAPI skeleton, DB models, Docker Compose | ⏳ Planned |
| **2 — Document Parsing** | PDF/DOCX ingestion and text extraction | ⏳ Planned |
| **3 — NLP Extraction** | NER, skill taxonomy, entity linking | ⏳ Planned |
| **4 — LLM Integration** | LLM summarization, feedback generation | ⏳ Planned |
| **5 — Semantic Search** | Vector embeddings, JD matching | ⏳ Planned |
| **6 — Frontend MVP** | Upload UI, results dashboard | ⏳ Planned |
| **7 — Auth & Security** | JWT auth, rate limiting, RBAC | ⏳ Planned |
| **8 — Production Hardening** | Testing, monitoring, deployment | ⏳ Planned |

---

## Contributing

Contributions are welcome once the project reaches an early development milestone. In the meantime, feel free to open issues for feature requests or architectural discussions.

Please read [AGENTS.md](AGENTS.md) before contributing — it contains project-wide coding standards and conventions that all contributors (human and AI) must follow.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
