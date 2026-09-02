"""Utilities for loading SQL query files."""

from pathlib import Path


def load_sql(sql_file: str | Path) -> str:
    """Read a non-empty SQL query from a ``.sql`` file."""
    path = Path(sql_file)
    if path.suffix.lower() != ".sql":
        message = f"Expected a .sql file, received: {path}"
        raise ValueError(message)
    if not path.is_file():
        raise FileNotFoundError(path)

    query = path.read_text(encoding="utf-8")
    if not query.strip():
        message = f"SQL file is empty: {path}"
        raise ValueError(message)
    return query
