# Week 3 Weekly Assessment: ML/AI Fundamentals + Decision Framework

## Setup (Windows PowerShell)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # then add your GEMINI_API_KEY and trainer's prices
```

## Run
| Step | Command | Output |
|---|---|---|
| Create data | `python make_data.py` | tickets_raw.csv (46 rows) |
| Task 1 | `python task1.py` | tickets_clean.csv, audit, metrics, KMeans |
| Task 2 | `python task2.py` | comparison_table.md |
| Task 3 | `python task3.py` | 4 result tables (needs API key for parts 3 and 4) |
| Task 4 | open `task4_decision_table.md`, `task4_proposal.md` | |

## Decisions
- **Task 1:** raw data has 46 rows: 38 unique, 5 duplicates (compared case-insensitively), 5 missing values and mixed casing. After cleaning: 38 rows. With only 38 tickets, the 20% test set is 8 tickets, so accuracy moves in steps of 0.125 (3/8 = 0.38 baseline, 7/8 = 0.88 model). `random_state=4` is fixed so results are repeatable.
- **Task 2:** `all-MiniLM-L6-v2` embeddings and my own numpy cosine similarity. Keyword search uses exact word overlap.
- **Task 3:** Gemini API for temperature/hallucination; prices are read from `.env` (use your trainer's prices).
- **Task 4:** Plain code for exact problems, ML/RAG for the rest, humans review risky outputs.

## Git
```
git init
git add .
git commit -m "Week 3 assessment: Task 1 data audit and model"
```
(.env is ignored by .gitignore.)
