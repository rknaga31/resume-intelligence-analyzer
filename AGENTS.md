# AGENTS.md — Project-Wide AI Agent Instructions

> This file contains authoritative instructions for all AI coding agents (Copilot, Antigravity, Claude, Gemini, Cursor, etc.)
> working on the **Resume Intelligence Analyzer** repository. Read this file in full before making any changes.

---

## 1. Project Identity

| Field | Value |
|---|---|
| **Repository** | `resume-intelligence-analyzer` |
| **GitHub** | `https://github.com/rknaga31/resume-intelligence-analyzer` |
| **Primary Language** | Python (backend/ML), TypeScript (frontend) |
| **Status** | 🚧 Early Development |

---

## 2. Absolute Rules (Never Violate)

1. **Never commit secrets.** Never write real API keys, passwords, tokens, database URLs with credentials, or private keys into any source file, test fixture, or commit. Use `.env.example` as the template and `.env` (gitignored) for real values.

2. **Never delete existing working code** without explicit human approval.

3. **Never force-push** to `main` or any protected branch.

4. **Never add fake metrics or performance claims.** If a feature is not implemented, say so. Use `TODO`, `NotImplementedError`, or `raise NotImplementedError("Not implemented yet")`.

5. **Never commit `.env`** or any file matching `.env.*` (except `.env.example`).

6. **Never store PII.** Uploaded resumes must be treated as sensitive. Do not log resume content, do not persist parsed text beyond job scope unless explicitly intended.

---

## 3. Repository Structure

Agents must respect and maintain this structure:

```
backend/         ← FastAPI application (Python)
frontend/        ← React / Next.js application (TypeScript)
ml/              ← ML/NLP pipeline modules (Python)
tests/           ← All test suites (unit / integration / e2e)
docs/            ← Human-readable documentation
scripts/         ← Dev ops, data migration, utility scripts
.github/
  workflows/     ← GitHub Actions CI/CD pipelines
```

Do **not** create top-level directories outside this structure without discussion.

---

## 4. Language & Framework Standards

### Python (backend & ml)
- **Version**: Python 3.11+
- **Style**: PEP 8, enforced by `ruff` (formatter + linter)
- **Types**: All public functions must have full type annotations
- **Async**: Use `async/await` throughout FastAPI handlers; avoid blocking I/O in async context
- **Framework**: FastAPI with Pydantic v2 for validation
- **ORM**: SQLAlchemy 2.0 with async sessions (`AsyncSession`)
- **Imports**: Always use absolute imports within `app/`
- **Docstrings**: Google-style docstrings for all public classes and functions

### TypeScript (frontend)
- **Version**: TypeScript 5+ with strict mode enabled
- **Framework**: Next.js 14+ (App Router)
- **Style**: ESLint + Prettier (auto-configured)
- **Components**: Functional components only, no class components
- **State**: Server Components by default; use client components (`"use client"`) only when necessary
- **API calls**: Use centralized API client in `frontend/src/lib/api.ts`

---

## 5. Security Requirements

- All file uploads must be validated for MIME type AND magic bytes — not filename alone
- Maximum upload size must be enforced at the API layer (`MAX_UPLOAD_SIZE_MB` from env)
- Uploaded resumes are temporary; schedule deletion after processing
- All database queries must use parameterized statements (SQLAlchemy handles this — never use raw string interpolation)
- JWT tokens must be validated on every protected route
- CORS origins must come from the `ALLOWED_ORIGINS` environment variable

---

## 6. Git & Branching Conventions

### Branch Naming
```
feature/<short-description>     # New features
fix/<short-description>         # Bug fixes
chore/<short-description>       # Maintenance, deps, config
docs/<short-description>        # Documentation only
test/<short-description>        # Test additions/fixes
ml/<short-description>          # ML/NLP pipeline work
refactor/<short-description>    # Code restructuring
```

### Commit Message Format (Conventional Commits)
```
<type>(<scope>): <short description>

[optional body — explain WHY, not WHAT]

[optional footer — issue refs, breaking changes]
```

**Types**: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`, `perf`, `ci`, `build`

**Examples**:
```
feat(api): add resume upload endpoint with MIME validation
fix(ml): handle empty skills section in NER extractor
chore(deps): update fastapi to 0.115.x
test(parser): add unit tests for PDF extraction edge cases
```

---

## 7. Testing Requirements

- **Coverage target**: ≥ 80% on all new code in `backend/` and `ml/`
- Unit tests live in `tests/unit/`
- Integration tests (DB, external APIs with mocks) live in `tests/integration/`
- E2E tests (Playwright) live in `tests/e2e/`
- Every PR must pass all tests in CI before merging

### Test Naming
```python
def test_<component>_<scenario>_<expected_result>():
    # e.g.
def test_resume_parser_empty_pdf_raises_value_error():
```

---

## 8. ML / NLP Development Standards

- All ML modules must be importable without side effects (no model loading at import time)
- Model weights are never committed — use `HuggingFace Hub`, `S3`, or document where to obtain them
- Embeddings are never stored as plain files in the repo — use the configured vector database
- LLM calls must go through the abstraction layer in `ml/llm/` — never call OpenAI / Anthropic directly from API routes
- All LLM prompts must be stored in dedicated prompt files (`.txt` or `.jinja2`), not hardcoded in Python

---

## 9. Documentation Standards

- Every new module must have a `README.md` explaining its purpose and how to use it
- All API endpoints must be documented via FastAPI's built-in OpenAPI annotations (`summary`, `description`, `response_model`)
- Architecture decisions must be documented in `docs/architecture/` as ADRs (Architecture Decision Records)
- Update `docs/` when behavior changes — stale docs are worse than no docs

---

## 10. CI/CD (GitHub Actions)

All pull requests targeting `main` must pass:
1. `ruff check` — Python lint
2. `ruff format --check` — Python formatting
3. `mypy` — Python static type checking
4. `pytest` — backend unit + integration tests
5. `tsc --noEmit` — TypeScript compilation check
6. `eslint` — TypeScript lint
7. `docker build` — Docker image build validation

Agents should not merge PRs that fail CI.

---

## 11. What Agents Should NOT Do

- Do not generate placeholder stub files and call it "done" — stubs are acceptable only if clearly marked `# TODO: implement`
- Do not create duplicate abstractions — check existing code first
- Do not change database schema migrations without running and testing the migration
- Do not add new dependencies without adding them to `requirements.txt` (backend) or `package.json` (frontend)
- Do not silently catch exceptions — log them and re-raise or return proper error responses
- Do not use `print()` for logging — use the configured logger (`from app.core.logging import logger`)

---

## 12. Context for AI Agents

When you are asked to implement a feature in this repository:

1. **Read relevant existing code first** — understand the patterns in use
2. **Check this AGENTS.md** — ensure your implementation follows the standards above
3. **Check `.env.example`** — understand all available configuration variables before hardcoding values
4. **Follow the directory structure** — put files where they belong
5. **Write tests** — every non-trivial function should have a corresponding test
6. **Document your work** — update READMEs and docstrings

If a task is ambiguous, output a clear question rather than guessing.

---

*Last updated: 2026-08-12 | Maintainer: rknaga31*
