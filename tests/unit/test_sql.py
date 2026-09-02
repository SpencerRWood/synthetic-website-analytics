import pytest

from synthetic_website_analytics.data.sql import load_sql


def test_load_sql_returns_query(tmp_path) -> None:
    sql_file = tmp_path / "query.sql"
    sql_file.write_text("SELECT 1;", encoding="utf-8")

    assert load_sql(sql_file) == "SELECT 1;"


def test_load_sql_rejects_non_sql_files(tmp_path) -> None:
    text_file = tmp_path / "query.txt"
    text_file.write_text("SELECT 1;", encoding="utf-8")

    with pytest.raises(ValueError, match=r"Expected a \.sql file"):
        load_sql(text_file)
