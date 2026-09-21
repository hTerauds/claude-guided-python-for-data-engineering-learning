# Roadmap: Python → Mid-Level Data Engineer

Starting point: Days 1-3 already covered CSV, JSON, SQLite, functions/modules, and REST APIs. This roadmap builds from there toward mid-level DE job readiness. Treat phases as rough sequencing, not rigid deadlines — pace it to what your sessions actually cover.

## Phase 1: Solidify Python Foundations (in progress)
- [x] File I/O: CSV, JSON
- [x] Data structures: dict, defaultdict, Counter, list/dict comprehensions
- [x] Functions, modules, `if __name__ == "__main__"`
- [x] `try/except` error handling
- [x] Git & GitHub basics
- [ ] Classes & OOP basics (when you need to model something stateful — a pipeline config, a connection wrapper)
- [ ] Virtual environments (`venv`) and `requirements.txt` — isolating project dependencies
- [ ] Type hints (`def f(x: int) -> str:`) — increasingly expected in professional codebases
- [ ] Basic testing with `pytest` — writing a test for one of your existing pipeline functions is a good first exercise

## Phase 2: SQL Depth
- [x] Basic `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `COUNT`/`SUM`
- [ ] `JOIN`s (inner, left, right) — critical, most real queries touch multiple tables
- [ ] Subqueries and CTEs (`WITH ... AS`)
- [ ] Window functions (`ROW_NUMBER()`, `RANK()`, `LAG`/`LEAD`) — very common in DE interviews
- [ ] Indexes — what they are, when they help, `EXPLAIN QUERY PLAN`
- [ ] A real server-based DB (PostgreSQL locally via Docker) — SQLite is great for learning but not what employers run in production

## Phase 3: Data Handling at Scale
- [ ] `pandas` — DataFrames, filtering, groupby, merging; this is the standard tool for anything beyond a few thousand rows
- [ ] Working with Parquet (columnar format — faster and more space-efficient than CSV/JSON for large data)
- [ ] Data validation — `pydantic` or `great_expectations` for catching bad data before it enters a pipeline (a more structured version of the `.get()`/`try-except` instincts you've already built)

## Phase 4: Pipelines & Orchestration
- [ ] ETL vs. ELT concepts
- [ ] Basic orchestration with `Apache Airflow` (or a lighter alternative like `Prefect`) — scheduling and chaining the kind of scripts you've already been writing
- [ ] Idempotency — designing pipelines that are safe to re-run (you've already touched this with `DELETE FROM` before re-insert)
- [ ] Logging properly (Python's `logging` module instead of `print()`)

## Phase 5: Cloud & Infrastructure Basics
- [ ] Pick one cloud provider (AWS is most in-demand for DE roles) — object storage (S3), a managed data warehouse (Redshift or BigQuery if going GCP)
- [ ] Docker basics — containerizing a script/pipeline
- [ ] Environment variables / secrets management (never hardcode credentials — relevant the moment you started using API calls)

## Phase 6: Data Modeling & Warehousing
- [ ] Star schema / dimensional modeling — the standard way data warehouses are structured
- [ ] Normalization vs. denormalization tradeoffs
- [ ] Slowly changing dimensions (a classic DE interview topic)

## Phase 7: Portfolio & Job Readiness
- [ ] One end-to-end portfolio project on GitHub: fetch from a real API or public dataset → validate → transform → load into a real database → orchestrate with a schedule → document with a README
- [ ] Comfortable explaining every script you've written — interviews often probe *why*, not just *what*
- [ ] Practice SQL problems (window functions, joins) on a site like LeetCode/StrataScratch — DE interviews lean SQL-heavy
- [ ] Mock system-design-lite questions: "how would you design a pipeline to ingest X daily" — mostly about tradeoffs, not perfect answers

## Notes
- This is sequenced but not strict — some phases (SQL depth, pandas) matter more early than others (cloud, orchestration) depending on what jobs you're targeting.
- Mid-level (vs. junior) is mostly distinguished by: SQL fluency, comfort with production concerns (idempotency, logging, error handling, testing), and having shipped something end-to-end — not by knowing more tools in isolation.
