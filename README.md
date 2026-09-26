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

For local database access, authenticate to Infisical and run Python through the
repository launcher. It opens a temporary SSH tunnel and expects a valid
`DBT_PASSWORD` in `Infrastructure Dev/dev:/synthetic-website-analytics`.
The tunnel closes when the command exits. No local `.env` is required once the
Infisical credential has been validated.

```sh
infisical login --domain=https://dev-infisical.woodhost.cloud/api --method=user --interactive
scripts/dev python -c 'from sqlalchemy import text; from synthetic_website_analytics.data import DatabaseConnector; c = DatabaseConnector.from_env(); conn = c.engine.connect(); print(conn.execute(text("SELECT 1")).scalar()); conn.close(); c.dispose()'
```

The launcher requires the `swood-server` SSH alias in your local SSH config.
Set `DBT_TUNNEL_PORT` if port 25435 is already in use.

## Database queries

Set `DBT_HOST`, `DBT_PORT`, `DBT_USER`, and `DBT_PASSWORD` in the process
environment. Set `DBT_DATABASE` to target a specific database; it defaults to `postgres`.
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
