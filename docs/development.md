# Developer Setup & Contribution Guide

## 1. Prerequisites

- Python 3.11+ (Python 3.13 tested)
- Node.js 20+ (v20.18.0 tested)
- Git

---

## 2. Local Setup

### Backend (Python / FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run FastAPI dev server
uvicorn app.main:app --reload --port 8000
```

### Frontend (React / Next.js / TypeScript)
```bash
cd frontend
npm install
npm run dev
```

---

## 3. Running Tests & Linters

```bash
# Backend unit & integration tests
pytest tests/ -v

# Code formatting & linting
ruff check backend/ ml/ tests/
ruff format --check backend/ ml/ tests/

# Frontend typecheck & lint
cd frontend
npx tsc --noEmit
npm run lint
```
