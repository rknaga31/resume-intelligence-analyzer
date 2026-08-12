# Evaluation Benchmark Suite — Resume Intelligence Analyzer

## 1. Evaluation Philosophy

To ensure reliability, scoring accuracy, and NLP extraction precision, the Resume Intelligence Analyzer includes a synthetic evaluation suite in `tests/`.

> ⚠️ **Data Privacy Notice**: *All evaluation test data uses synthetic, fully fictional candidate resumes and job descriptions. No real candidate PII is stored or used for benchmarks.*

---

## 2. Evaluation Metrics

| Metric | Target Threshold | Method |
|---|---|---|
| **Contact Entity Extraction Precision** | \(\ge 98\%\) | Exact match vs synthetic ground truth |
| **Section Boundary Recall** | \(\ge 95\%\) | Header classification accuracy across 50 test resumes |
| **Skill Extraction F1-Score** | \(\ge 90\%\) | Micro F1-score on skill taxonomy matching |
| **Semantic Matching Consistency** | \(\ge 92\%\) | Cosine similarity ranking correlation |
| **Quantified Achievement Detection Accuracy** | \(\ge 95\%\) | Binary metric classification on bullet points |
| **Prompt Injection Resilience** | \(100\%\) | 0% instruction execution on adversarial injection test suite |

---

## 3. Synthetic Benchmark Datasets

Located in `tests/data/`:
- `synthetic_resumes.json`: 25 structured test resumes across Software Engineering, AI/ML, Data Science, DevOps, and Product Management.
- `synthetic_jobs.json`: 10 standardized target job descriptions with ground truth required/preferred skills.
- `adversarial_injections.json`: 15 prompt injection attack payloads embedded inside fake resume PDF/TXT documents.

---

## 4. Running Benchmarks

```bash
# Run complete evaluation benchmark suite
pytest tests/unit/test_evaluation_benchmark.py -v
```
