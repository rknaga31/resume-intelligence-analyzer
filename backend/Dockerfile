# =============================================================================
# Multi-stage Production Dockerfile — Backend API & ML Engine
# =============================================================================

# --- Builder Stage ---
FROM python:3.11-slim AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
RUN /install/bin/python -m spacy download en_core_web_sm

# --- Final Runner Stage ---
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000

# Security: non-root user
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app

COPY --from=builder /install /usr/local

# Copy application source and ML pipeline
COPY backend/app /app/app
COPY ml /app/ml

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
