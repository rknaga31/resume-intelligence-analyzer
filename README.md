# Resume Intelligence Analyzer

> **Status: ✅ Live — Full-stack AI resume analysis platform**

An AI-powered platform that transforms resumes into structured intelligence — deep NLP extraction, semantic job-description matching, ATS scoring, and LLM-generated career insights.

---

## Features

### Core Analysis
- ✅ Multi-format resume parsing — PDF, DOCX, TXT
- ✅ Named entity extraction — skills, roles, companies, education, certifications
- ✅ Section classification across 15+ resume header patterns
- ✅ Extensible 15-category technical skill taxonomy
- ✅ ATS-style compatibility scoring with explainable breakdown
- ✅ Achievement impact scoring engine

### AI / LLM Capabilities
- ✅ Multi-LLM support — OpenAI GPT-4o, Anthropic Claude, Google Gemini
- ✅ Prompt-sandboxed LLM reasoning layer
- ✅ Bullet-point improvement suggestions
- ✅ Transformer semantic vector matching (`all-MiniLM-L6-v2`)
- ✅ Skill gap analysis against job descriptions

### Platform
- ✅ JWT authentication — register, login, token refresh
- ✅ Secure file upload with MIME + magic-byte validation
- ✅ REST API with OpenAPI / Swagger docs (`/docs`)
- ✅ Next.js 14 frontend — upload flow, analysis progress, results dashboard
- ✅ Docker Compose for local full-stack development

### Infrastructure
- ✅ Multi-stage production Dockerfiles (backend + frontend)
- ✅ GitHub Actions CI/CD — lint, type-check, test, Docker build
- ✅ Render Blueprint for one-click backend + PostgreSQL deploy
- ✅ Vercel config for one-click frontend deploy
- ✅ Unit + integration test suite (pytest)

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 14 (App Router), React 19, TypeScript, Tailwind CSS |
| **Backend API** | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0 async |
| **Database** | PostgreSQL 15+ (primary), SQLite (local dev fallback) |
| **ML / NLP** | spaCy, Transformers (HuggingFace `all-MiniLM-L6-v2`) |
| **LLMs** | OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, Google Gemini 1.5 Pro |
| **Document Parsing** | pdfplumber, python-docx, PyMuPDF |
| **Auth** | JWT (python-jose), bcrypt |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Testing** | pytest, pytest-asyncio |

---

## Project Structure

```
resume-intelligence-analyzer/
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── api/v1/         # Route handlers (analysis, auth, health)
│   │   ├── core/           # Config, security (JWT), logging
│   │   ├── db/             # SQLAlchemy models, async session
│   │   ├── schemas/        # Pydantic v2 request/response models
│   │   └── services/       # Business logic (auth, analysis)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Next.js 14 application
│   ├── src/
│   │   ├── app/            # App Router pages (/, /analyze, /results)
│   │   ├── components/     # Reusable UI components
│   │   └── lib/            # API client, utilities
│   ├── package.json
│   └── Dockerfile
├── ml/                     # ML & NLP pipeline
│   ├── parsers/            # Document parsing + section detection
│   ├── extractors/         # NER and contact extraction
│   ├── llm/                # LLM providers (OpenAI, Anthropic, Gemini)
│   └── scoring/            # ATS analyzer + scorer
├── tests/
│   ├── unit/               # Unit tests
│   └── integration/        # API integration tests
├── docs/                   # Architecture docs, ADRs, roadmap
├── .github/workflows/      # GitHub Actions CI/CD
├── docker-compose.yml      # Local full-stack dev environment
├── render.yaml             # Render.com deploy blueprint
└── .env.example            # Environment variable template
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+ and npm
- Docker Desktop

### Quick Start (Docker Compose — recommended)

```bash
# 1. Clone the repository
git clone https://github.com/rknaga31/resume-intelligence-analyzer.git
cd resume-intelligence-analyzer

# 2. Configure environment
cp .env.example .env
# Edit .env — add your LLM API key (OPENAI_API_KEY or ANTHROPIC_API_KEY)

# 3. Start everything
docker compose up --build

# Backend API:  http://localhost:8000
# API Docs:     http://localhost:8000/docs
# Frontend:     http://localhost:3000
```

### Manual Setup

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

---

## Environment Variables

Copy `.env.example` to `.env`. Required variables:

| Variable | Description |
|---|---|
| `APP_SECRET_KEY` | 32+ random bytes — `openssl rand -hex 32` |
| `JWT_SECRET_KEY` | 32+ random bytes — `openssl rand -hex 32` |
| `DATABASE_URL` | PostgreSQL connection string |
| `OPENAI_API_KEY` | Or `ANTHROPIC_API_KEY` / `GOOGLE_API_KEY` |
| `ALLOWED_ORIGINS` | CORS — your frontend URL |

See [`.env.example`](.env.example) for the full reference.

---

## Deployment

### Frontend → Vercel

1. Import repo at [vercel.com/new](https://vercel.com/new)
2. Set **Root Directory** = `frontend`
3. Add env var: `NEXT_PUBLIC_API_URL` = your backend URL
4. Deploy

### Backend → Render (Blueprint)

1. Go to [dashboard.render.com/blueprints](https://dashboard.render.com/blueprints)
2. **New Blueprint Instance** → connect this repo
3. Render reads `render.yaml` and provisions the FastAPI service + PostgreSQL
4. Set secret env vars in the Render dashboard (LLM keys, `ALLOWED_ORIGINS`)

---

## Roadmap

| Phase | Description | Status |
|---|---|---|
| **0 — Repository Setup** | Scaffold project, CI/CD, documentation | ✅ Done |
| **1 — Core Infrastructure** | FastAPI, DB models, Docker Compose | ✅ Done |
| **2 — Document Parsing** | PDF/DOCX ingestion and text extraction | ✅ Done |
| **3 — NLP Extraction** | NER, skill taxonomy, entity linking | ✅ Done |
| **4 — LLM Integration** | LLM summarization, feedback generation | ✅ Done |
| **5 — Semantic Search** | Vector embeddings, JD matching | ✅ Done |
| **6 — Frontend MVP** | Upload UI, results dashboard | ✅ Done |
| **7 — Auth & Security** | JWT auth, MIME validation, security headers | ✅ Done |
| **8 — Production Hardening** | Testing, Docker, CI/CD, deploy configs | ✅ Done |
| **9 — Multi-Doc & ATS Integrations** | Batch analysis, LinkedIn import, webhooks | 🔜 Next |

---

## License

MIT — see [LICENSE](LICENSE).
