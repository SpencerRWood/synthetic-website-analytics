"""PostgreSQL connection and query helpers."""

from collections.abc import Mapping
from os import getenv
from pathlib import Path
from typing import Any, Self

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.engine import Engine

from .sql import load_sql


class DatabaseConnector:
    """Run PostgreSQL queries and return their results as data frames."""

    def __init__(self, database_url: str | URL) -> None:
        self._engine = create_engine(database_url)

    @property
    def engine(self) -> Engine:
        """Return the underlying SQLAlchemy engine."""
        return self._engine

    @classmethod
    def from_env(cls, env_file: str | Path = ".env") -> Self:
        """Create a connector from ``DATABASE_URL`` or PostgreSQL variables."""
        load_dotenv(dotenv_path=env_file)

        database_url = getenv("DATABASE_URL")
        if database_url:
            return cls(database_url)

        port_value = _first_environment_value(("DBT_PORT", "PGPORT")) or "5432"
        try:
            port = int(port_value)
        except ValueError as error:
            message = "DBT_PORT or PGPORT must be an integer."
            raise ValueError(message) from error

        url = URL.create(
            "postgresql+psycopg",
            username=_required_environment_value(("DBT_USER", "PGUSER")),
            password=_required_environment_value(("DBT_PASSWORD", "PGPASSWORD")),
            host=_required_environment_value(("DBT_HOST", "PGHOST")),
            port=port,
            database=_first_environment_value(("DBT_DATABASE", "PGDATABASE"))
            or "postgres",
        )
        return cls(url)

    def execute_sql(
        self,
        sql_file: str | Path,
        params: Mapping[str, Any] | None = None,
    ) -> pd.DataFrame:
        """Execute a SQL file and return the result as a pandas data frame."""
        query = load_sql(sql_file)
        return pd.read_sql_query(text(query), self._engine, params=params)

    def dispose(self) -> None:
        """Release database connections held by the engine."""
        self._engine.dispose()


def _first_environment_value(names: tuple[str, ...]) -> str | None:
    for name in names:
        value = getenv(name)
        if value:
            return value
    return None


def _required_environment_value(names: tuple[str, ...]) -> str:
    value = _first_environment_value(names)
    if value is not None:
        return value
    message = f"Missing required database environment variable: {' or '.join(names)}."
    raise ValueError(message)
