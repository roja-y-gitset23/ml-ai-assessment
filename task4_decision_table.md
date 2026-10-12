# Task 4: Solution Decision Framework

| # | Problem | Input type | Output type | Constraints (latency / cost / explainability) | Tool choice | Human review? | AI allowed? |
|---|---|---|---|---|---|---|---|
| 1 | GST calculation on invoices | Structured numbers (amount, GST rate) | Exact number | Instant / near-zero cost / must be fully explainable and exactly correct | Plain code (formula: amount × rate) | No, needs only automated tests | **NO. Do not use AI.** A rule gives the exact answer every time; an LLM can make arithmetic errors |
| 2 | Current leave balance of an employee | Employee ID | Single number from HR system | Instant / cheap / must be exact and up to date | Database query / HRMS API | No | **NO. Do not use AI.** It is a lookup; AI could guess or give an old number |
| 3 | Ranking resumes for a role | Unstructured text (resumes + job description) | Ranked list with scores | Seconds / moderate / must be explainable and fair | Embeddings + similarity score (+ simple rule filters such as skills and years) | **YES.** A recruiter makes the final decision (bias and fairness risk) | Yes, only to shortlist, never to reject automatically |
| 4 | Answering questions from a 60-page contract | Long unstructured text (PDF) + natural-language question | Short text answer with clause reference | Few seconds / moderate cost per query / answers must cite the source clause | RAG: chunk + embed + retrieve + LLM answer | **YES.** Legal team reviews important or risky answers | Yes, as an assistant; not as legal advice |
| 5 | Forecasting next month's sales | Historical numbers (time series) | One number or a range | Batch (minutes) / low / explainable trend and seasonality | Statistical or ML time-series model (moving average, Prophet or regression) vs. baseline | **YES.** Manager approves the plan | Yes (ML, not LLM) |

## Summary
- **AI should NOT be used:** GST calculation (#1) and leave balance (#2). Both need exact answers from rules or data.
- **Human must review:** resume ranking (#3), contract answers (#4), sales forecast (#5).
