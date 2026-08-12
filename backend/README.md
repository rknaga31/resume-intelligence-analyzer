# backend/

FastAPI application — REST API server for the Resume Intelligence Analyzer.

## Planned Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app factory
│   ├── api/
│   │   ├── deps.py       # Shared dependencies (DB session, current user)
│   │   └── v1/
│   │       ├── router.py # API v1 router
│   │       ├── resumes.py
│   │       ├── analysis.py
│   │       └── auth.py
│   ├── core/
│   │   ├── config.py     # Settings (Pydantic BaseSettings)
│   │   ├── security.py   # JWT, password hashing
│   │   └── logging.py    # Structured logging setup
│   ├── db/
│   │   ├── base.py       # SQLAlchemy declarative base
│   │   ├── session.py    # Async session factory
│   │   ├── models/       # ORM models
│   │   └── migrations/   # Alembic migrations
│   ├── schemas/          # Pydantic request/response schemas
│   └── services/         # Business logic layer
├── requirements.txt
├── requirements-dev.txt
└── Dockerfile
```

## Technology

- Python 3.11+
- FastAPI + Pydantic v2
- SQLAlchemy 2.0 (async)
- Alembic (migrations)
- uvicorn (ASGI server)

See [AGENTS.md](../AGENTS.md) for coding standards.
