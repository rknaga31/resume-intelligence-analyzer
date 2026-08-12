# tests/

Test suite for the Resume Intelligence Analyzer.

## Structure

```
tests/
├── unit/           # Fast, isolated unit tests (no DB, no network)
├── integration/    # Tests with real DB / mocked external APIs
└── e2e/            # End-to-end tests (Playwright)
```

## Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests (requires running PostgreSQL + Redis)
pytest tests/integration/

# With coverage report
pytest --cov=app --cov-report=html tests/
```

## Coverage Target

≥ 80% coverage on all code in `backend/` and `ml/`. See [AGENTS.md](../AGENTS.md) for testing standards.
