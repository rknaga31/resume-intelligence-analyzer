# Privacy Policy & PII Protection Guidelines

## 1. Candidate Privacy Statement

Resumes contain sensitive Personally Identifiable Information (PII) including names, email addresses, telephone numbers, home addresses, and employment history.

The **Resume Intelligence Analyzer** is engineered with privacy-by-design principles:

- **Zero Permanent Storage by Default**: Uploaded resume files are processed temporarily in memory and deleted immediately after analysis completes.
- **Zero PII Logging**: Application logs log technical metadata (request ID, processing time, status codes) and explicitly exclude candidate names, emails, phones, or raw document text.
- **No Third-Party Data Training**: Resume content sent to configured LLM providers is processed under zero-data-retention APIs (e.g. OpenAI API non-training terms).

---

## 2. PII Sanitization in Logs

Example of sanitized logging:
```json
{
  "timestamp": "2026-08-12T23:32:00Z",
  "level": "INFO",
  "event": "resume_parsed",
  "request_id": "req_88a1b2c3",
  "filename": "sanitized_document.pdf",
  "word_count": 520,
  "execution_time_ms": 142
}
```

No candidate name, phone number, email, or resume text is ever printed to stdout or written to log files.
