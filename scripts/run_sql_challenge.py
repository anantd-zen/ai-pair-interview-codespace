"""Run the current SQL challenge against a fresh in-memory DuckDB database."""

from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = ROOT / "sql"


def main() -> None:
    connection = duckdb.connect(":memory:")
    connection.execute((SQL_DIR / "schema.sql").read_text(encoding="utf-8"))
    connection.execute((SQL_DIR / "seed.sql").read_text(encoding="utf-8"))
    query = (SQL_DIR / "challenge.sql").read_text(encoding="utf-8")

    if not query.strip() or all(
        not line.strip() or line.lstrip().startswith("--") for line in query.splitlines()
    ):
        raise SystemExit("sql/challenge.sql does not contain a query yet")

    result = connection.execute(query)
    columns = [description[0] for description in result.description]
    print(" | ".join(columns))
    for row in result.fetchall():
        print(" | ".join("NULL" if value is None else str(value) for value in row))


if __name__ == "__main__":
    main()

