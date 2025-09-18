# NutritionAnalysis FastAPI

Modular FastAPI app using SQLite, SQLAlchemy 2.0, Pydantic v2, and mypy strict.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
```

## Run

```bash
uvicorn app.main:app --reload
```

## Type-check

```bash
mypy .
```

## Lint

```bash
ruff check .
```
