# synthetic-website-analytics

Analytics workspace for exploring synthetic website data, organized by the
major stages of the website analytics lifecycle.

## Repository layout

- `src/`: importable Python package code.
- `src/synthetic_website_analytics/data/`: data-access interfaces and shared
  SQL-related utilities.
- `src/synthetic_website_analytics/{traffic,acquisition,engagement,conversion,retention,journeys}/`:
  analysis modules grouped by analytics domain.
- `sql/`: saved SQL queries, organized by the same analytics domains.
- `notebooks/`: exploratory Jupyter notebooks.
- `tests/`: automated tests.
- `artifacts/`: locally generated analysis outputs; its contents are ignored by
  Git.

## Setup

Install the project and development dependencies:

```sh
uv sync --group dev
```

Use a `.env` file for local environment configuration. It is intentionally not
tracked.

## Database queries

Set `DBT_HOST`, `DBT_PORT`, `DBT_USER`, and `DBT_PASSWORD` in `.env`. Set
`DBT_DATABASE` to target a specific database; it defaults to `postgres`.
`DATABASE_URL` is also supported and takes precedence over the individual
variables.

```python
from synthetic_website_analytics.data import DatabaseConnector

connector = DatabaseConnector.from_env()
data_frame = connector.execute_sql("sql/traffic/weekly_visitors.sql")
connector.dispose()
```

Pass named query parameters with `params`, for example
`connector.execute_sql(path, params={"start_date": "2026-01-01"})`.

## Checks

```sh
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```
