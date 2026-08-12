# Deployment Guide — Resume Intelligence Analyzer

## 1. Local Docker Compose Deployment

The application is containerized with multi-stage Dockerfiles.

```bash
# Clone repository
git clone https://github.com/rknaga31/resume-intelligence-analyzer.git
cd resume-intelligence-analyzer

# Configure environment variables
cp .env.example .env

# Launch services (PostgreSQL, Redis, FastAPI Backend, Next.js Frontend)
docker compose up -d --build

# Access application:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# OpenAPI Docs: http://localhost:8000/docs
```

---

## 2. Cloud Production Deployment

Recommended architecture:
- **Frontend**: Vercel / Netlify / AWS CloudFront + S3
- **Backend API**: AWS ECS / GCP Cloud Run / Render (FastAPI Docker container)
- **Database**: Managed PostgreSQL (AWS RDS / GCP Cloud SQL / Neon / Supabase)
- **Vector DB**: Pinecone / Qdrant Cloud / Managed Weaviate
