# Scoring Methodology — Resume Intelligence Analyzer

## 1. Score Dimensions Overview

All scores produced by the Resume Intelligence Analyzer range from `0` to `100` and are derived from explicit, deterministic mathematical rules combined with semantic embedding calculations.

| Dimension | Weight | Description |
|---|---|---|
| **ATS Compatibility** | 25% | Standard section headers, contact completeness, formatting simplicity, bullet formatting |
| **Job Match Score** | 35% | Keyword evidence, semantic embedding similarity, skill match coverage |
| **Achievement Impact** | 25% | Presence of quantifiable metrics (%, $, scale, latency, accuracy, volume) |
| **Skill Relevance** | 15% | Breadth and depth of technical/soft skills aligned with target domain |

---

## 2. ATS-Style Compatibility Index

> ⚠️ **Disclaimer**: *This is an AI-assisted ATS-style analysis and does not guarantee the behavior of a specific employer's proprietary ATS.*

### Formula Component Breakdown:
- **Contact Completeness (25 pts)**:
  - Email detected: +10
  - Phone detected: +5
  - Location detected: +5
  - LinkedIn/GitHub link detected: +5
- **Standard Section Headers (35 pts)**:
  - Summary / Objective: +5
  - Experience / Employment: +10
  - Skills / Competencies: +10
  - Education: +10
- **Formatting Complexity & Cleanliness (25 pts)**:
  - Standard bullet points: +10
  - Clean word count (300 - 1200 words): +10
  - No suspicious special characters or tables: +5
- **Date Consistency & Contact Formatting (15 pts)**:
  - Valid date ranges detected in experience: +15

---

## 3. Job Match Engine Methodology

The Overall Job Match Score combines four sub-metrics:

```text
Job Match Score = (Keyword_Match * 0.30) + (Semantic_Similarity * 0.30) 
                  + (Skill_Coverage * 0.30) + (Experience_Alignment * 0.10)
```

- **Skill Coverage Breakdown**:
  - `Matched Skill`: +1.0 point per required skill
  - `Partial / Related Skill`: +0.6 points per related skill (e.g. PyTorch ↔ TensorFlow)
  - `Missing Skill`: 0.0 points

---

## 4. Achievement Impact Index

The Achievement Impact score evaluates whether experience bullet points demonstrate measurable results rather than passive responsibility lists.

- **Quantification Metrics Detected**:
  - Percentages (`18%`, `35% increase`)
  - Scaling numbers (`10K daily users`, `5M records`)
  - Financial impact (`$50K saved`, `$1.2M revenue`)
  - Latency / Speed (`reduced latency by 200ms`)
  - Accuracy / Quality (`achieved 99.4% precision`)

- **Scoring**:
  - \(\ge 70\%\) of bullet points quantified: **90 - 100**
  - \(50\% - 69\%\) of bullet points quantified: **75 - 89**
  - \(25\% - 49\%\) of bullet points quantified: **50 - 74**
  - \(< 25\%\) of bullet points quantified: **< 50**
