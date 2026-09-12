from pathlib import Path

import pandas as pd
import pytest

from synthetic_website_analytics.data import DatabaseConnector


def test_connector_uses_dbt_environment_variables(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DBT_HOST", "database.example.test")
    monkeypatch.setenv("DBT_PORT", "5432")
    monkeypatch.setenv("DBT_USER", "analytics")
    monkeypatch.setenv("DBT_PASSWORD", "password")
    monkeypatch.setenv("DBT_DATABASE", "website")

    connector = DatabaseConnector.from_env("missing.env")

    assert connector.engine.url.drivername == "postgresql+psycopg"
    assert connector.engine.url.host == "database.example.test"
    assert connector.engine.url.port == 5432
    assert connector.engine.url.database == "website"
    assert connector.engine.url.username == "analytics"
    connector.dispose()


def test_connector_prefers_database_url(monkeypatch) -> None:
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql+psycopg://analytics:password@localhost:5432/website"
    )

    connector = DatabaseConnector.from_env("missing.env")

    assert connector.engine.url.database == "website"
    connector.dispose()


def test_connector_rejects_invalid_port(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DBT_PORT", "not-a-port")

    with pytest.raises(ValueError, match="DBT_PORT or PGPORT must be an integer"):
        DatabaseConnector.from_env("missing.env")


def test_connector_requires_connection_values(monkeypatch) -> None:
    for name in (
        "DATABASE_URL",
        "DBT_HOST",
        "PGHOST",
        "DBT_USER",
        "PGUSER",
        "DBT_PASSWORD",
        "PGPASSWORD",
    ):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(ValueError, match="DBT_USER or PGUSER"):
        DatabaseConnector.from_env("missing.env")


def test_connector_executes_loaded_query(monkeypatch, tmp_path: Path) -> None:
    sql_file = tmp_path / "query.sql"
    sql_file.write_text("SELECT 1;", encoding="utf-8")
    connector = DatabaseConnector("postgresql+psycopg://localhost/website")
    expected = pd.DataFrame({"value": [1]})

    def read_sql_query(query, engine, params):
        assert str(query) == "SELECT 1;"
        assert engine is connector.engine
        assert params == {"limit": 1}
        return expected

    monkeypatch.setattr(pd, "read_sql_query", read_sql_query)

    assert connector.execute_sql(sql_file, params={"limit": 1}) is expected
    connector.dispose()
