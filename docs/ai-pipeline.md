# AI & NLP Pipeline Architecture

## 1. Overview

The AI/NLP pipeline is the core intelligence engine of the application. It avoids single-step "Resume → LLM → Response" anti-patterns in favor of a multi-stage, deterministic-plus-probabilistic pipeline.

```text
Raw Resume Document (PDF / DOCX / TXT)
  │
  ├── 1. Text Extraction & Sanitization (MIME, Magic Bytes, Encoding cleanup)
  ├── 2. Section Boundary Detection (Classification into 15+ section headers)
  ├── 3. Information Extraction (NER: Name, Email, Phone, Degrees, Work bullets)
  ├── 4. Skill Taxonomy Classification (Exact, Alias, & Fuzzy match across 15 domains)
  ├── 5. Semantic Vector Encoding (SentenceTransformers `all-MiniLM-L6-v2`)
  ├── 6. Job Match Engine (Keyword + Vector Similarity + Skill Evidence)
  ├── 7. ATS & Achievement Impact Scoring (Deterministic metric quantification checks)
  └── 8. LLM Reasoning Layer (Prompt-sandboxed synthesis & bullet enhancement)
```

---

## 2. Document Processing & Section Classification

- **Section Detection**: Segments document into structured blocks by inspecting typography, line breaks, casing, and section headers.
- **Supported Headers**:
  - `Summary / Executive Profile / Objective`
  - `Skills / Core Competencies / Technical Stack`
  - `Work Experience / Employment History / Professional Experience`
  - `Projects / Major Achievements / Technical Portfolio`
  - `Education / Academic Background`
  - `Certifications / Licenses`
  - `Honors & Awards / Leadership`

---

## 3. Skill Taxonomy Engine

Skills are classified into an extensible JSON taxonomy (`ml/taxonomy/skills_taxonomy.json`) across 15 categories:

1. `AI / ML`: PyTorch, TensorFlow, Scikit-Learn, Keras, XGBoost, MLflow
2. `Data Science`: Pandas, NumPy, SciPy, Matplotlib, Polars, Statsmodels
3. `NLP`: spaCy, NLTK, HuggingFace Transformers, BERT, T5, LangChain
4. `Generative AI`: OpenAI API, LLMs, RAG, Vector DBs, Fine-tuning, Prompt Engineering
5. `Web Development`: HTML5, CSS3, Tailwind CSS, JavaScript, React, Next.js, Vue
6. `Backend`: Python, FastAPI, Django, Flask, Node.js, Express, Go, Java
7. `Databases`: PostgreSQL, MySQL, Redis, MongoDB, Pinecone, Qdrant, Weaviate
8. `Cloud`: AWS, GCP, Azure, Cloudflare, Serverless, Lambda, S3
9. `DevOps`: Docker, Kubernetes, CI/CD, GitHub Actions, Terraform, Nginx
10. `Cybersecurity`: OWASP, JWT, OAuth2, Cryptography, Identity Management
11. `Computer Vision`: OpenCV, YOLO, TorchVision, Image Processing
12. `Tools & IDEs`: Git, Linux, Bash, VSCode, PyCharm, JIRA
13. `Soft Skills`: Leadership, Communication, Problem Solving, Agile, Mentorship
14. `Domain Knowledge`: FinTech, HealthTech, E-Commerce, SaaS, MLOps
15. `Languages`: English, Spanish, French, German, Mandarin

---

## 4. Semantic Embedding & Vector Matching

- Embeddings are generated using `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions).
- Cosine similarity between resume section vectors \( \mathbf{v}_r \) and job criteria vectors \( \mathbf{v}_j \):
  \[
  \text{Similarity}(\mathbf{v}_r, \mathbf{v}_j) = \frac{\mathbf{v}_r \cdot \mathbf{v}_j}{\|\mathbf{v}_r\| \|\mathbf{v}_j\|}
  \]
- **Skill Graph Inference**: Identifies related skills when an exact skill isn't listed (e.g. `TensorFlow` listed on resume vs `PyTorch` in job description yields partial credit of ~0.85).

---

## 5. LLM Layer & Security Guardrails

- **Prompt Sandboxing**: Untrusted resume and job text are wrapped in explicit boundary tags:
  ```text
  <untrusted_document_content>
  ... resume text here ...
  </untrusted_document_content>
  ```
- **System Instruction Enforcement**: Instructs LLM to treat inner contents strictly as static data to be evaluated, ignoring any embedded instructions like `"Ignore previous instructions"`.
- **Validation**: LLM response must adhere to Pydantic JSON schemas. Malformed responses trigger automatic retry handlers.
