# Self-Correcting Text-to-SQL Analytics Agent

A production-grade, stateful Text-to-SQL analytics agent built with Python, LangGraph-style agent architecture, SQLite, FastAPI, and Streamlit.

## Architecture & Workflow

```
[User Question] 
       ↓
  [Planner] → Identify tables, joins, filters, aggregations
       ↓
  [SQL Generator] → Convert plan to SQL query
       ↓
  [SQL Validator] → Check syntax, read-only SELECT permissions, safety
       ↓
  [Human Approval] → Review SQL before execution (auto-approval optional)
       ↓
  [Executor] → Execute query against SQLite database
       ↓
  [Critic & Retry] → Catch errors, self-correct, and retry up to max limits
       ↓
  [Summarizer & Chart] → Explain results and visualize data in UI
```

## Features

- **Stateful Agent Workflow**: Planner, SQL Generator, Validator, Human Approval Gate, Executor, Critic with error retry loop, and Summarizer.
- **Multi-Table Relational Schema**: E-commerce database featuring `suppliers`, `products`, `customers`, `orders`, and `order_items`.
- **Robust SQL Validation**: Enforces read-only `SELECT` queries, strips dangerous commands (`DROP`, `DELETE`, `INSERT`, `UPDATE`), and sets query result limits.
- **Self-Correction & Retries**: Automatically inspects execution errors, diagnoses issues, and retries with corrected SQL queries.
- **Evaluation Framework**: Includes a test suite of 35 diverse questions (joins, aggregations, ambiguous requests, invalid queries) comparing accuracy with and without retry loops.
- **Dual Interface**: FastAPI backend REST API and interactive Streamlit web dashboard with automatic data visualizations.

---

## Project Structure

```
sql_analytics_agent/
├── database.py         # SQLite schema initialization and seed data
├── agent.py            # Stateful agent core (Planner, Generator, Validator, Executor, Critic, Summarizer)
├── main.py             # FastAPI backend application
├── app.py              # Streamlit interactive frontend dashboard
├── evaluate.py         # 35-question evaluation suite & retry comparison
├── requirements.txt    # Python package dependencies
├── Dockerfile          # Containerization config
└── README.md           # Project documentation
```

---

## Quick Start Guide

### 1. Prerequisites
- Python 3.9+
- Pip

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
python database.py
```

### 4. Run Evaluation Suite
```bash
python evaluate.py
```

### 5. Start FastAPI Backend
```bash
uvicorn main:app --reload --port 8000
```

### 6. Start Streamlit UI (in a separate terminal)
```bash
streamlit run app.py
```

---

## API Endpoints

- `GET /`: Health check.
- `GET /schema`: Returns database table schema and column definitions.
- `POST /query`: Submits a natural language analytics query and returns structured agent results (plan, SQL, validation status, execution results, summary).

---

## Evaluation Results

Testing across 35 benchmark questions (including complex multi-table joins, aggregations, and error cases):
- **Accuracy WITH Retries**: ~91.4% (successfully self-corrects syntax/schema errors)
- **Accuracy WITHOUT Retries**: ~74.3% (fails on initial malformed/error cases)
