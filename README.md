# synthetic-website-analytics

Analytics workspace for querying and communicating insights from the synthetic
website dataset. It complements the generator and dbt transformation projects
in the [Synthetic Website Analytics Platform](https://github.com/SpencerRWood/synthetic-website-analytics-platform).

## Repository layout

- `src/`: importable Python package code.
- `src/synthetic_website_analytics/data/`: data-access interfaces and shared
  SQL-related utilities.
- `src/synthetic_website_analytics/data/`: database connection and SQL-query
  utilities.
- `sql/`: saved queries for campaign, conversion, navigation, and performance
  analysis.
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
tracked; copy `.env.example` and replace its placeholder values.

## Database queries

Set `DBT_HOST`, `DBT_PORT`, `DBT_USER`, and `DBT_PASSWORD` in `.env`. Set
`DBT_DATABASE` to target a specific database; it defaults to `postgres`.
`DATABASE_URL` is also supported and takes precedence over the individual
variables.

```python
from synthetic_website_analytics.data import DatabaseConnector

connector = DatabaseConnector.from_env()
data_frame = connector.execute_sql("sql/performance/daily_performance.sql")
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
