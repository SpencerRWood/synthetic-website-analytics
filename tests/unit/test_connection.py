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
