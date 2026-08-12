# ml/

Machine Learning and NLP pipeline for the Resume Intelligence Analyzer.

## Planned Structure

```
ml/
├── parsers/          # Document parsing (PDF, DOCX, TXT)
│   ├── __init__.py
│   ├── base.py       # Abstract base parser
│   ├── pdf_parser.py
│   └── docx_parser.py
├── extractors/       # NLP entity extraction
│   ├── __init__.py
│   ├── skills.py     # Skill extraction and taxonomy mapping
│   ├── entities.py   # NER (spaCy-based)
│   └── timeline.py   # Work experience timeline reconstruction
├── embeddings/       # Vector embedding pipeline
│   ├── __init__.py
│   ├── encoder.py    # Text → vector encoder
│   └── store.py      # Vector DB interface
├── llm/              # LLM integration
│   ├── __init__.py
│   ├── base.py       # Abstract LLM interface
│   ├── openai.py     # OpenAI adapter
│   ├── anthropic.py  # Anthropic adapter
│   └── prompts/      # Prompt templates (.jinja2)
└── scoring/          # Matching and scoring
    ├── __init__.py
    └── jd_matcher.py # Job description similarity scoring
```

## Key Principles

- Models are never loaded at import time
- LLM calls only go through `ml/llm/` abstractions
- Prompts are stored in `ml/llm/prompts/`, never hardcoded
- No PII is logged

See [AGENTS.md](../AGENTS.md) for ML coding standards.
