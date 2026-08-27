from datetime import datetime
from pathlib import Path

import duckdb
import pytest


pytestmark = pytest.mark.sql_challenge
ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = ROOT / "sql"


def test_customer_revenue_report() -> None:
    connection = duckdb.connect(":memory:")
    connection.execute((SQL_DIR / "schema.sql").read_text(encoding="utf-8"))
    connection.execute((SQL_DIR / "seed.sql").read_text(encoding="utf-8"))
    query = (SQL_DIR / "challenge.sql").read_text(encoding="utf-8")

    if not query.strip() or all(
        not line.strip() or line.lstrip().startswith("--") for line in query.splitlines()
    ):
        pytest.fail("sql/challenge.sql does not contain a query yet")

    result = connection.execute(query)
    assert [column[0] for column in result.description] == [
        "region",
        "customer_id",
        "customer_name",
        "completed_order_count",
        "completed_revenue_cents",
        "latest_completed_at",
        "revenue_rank_in_region",
    ]
    assert result.fetchall() == [
        ("east", 2, "Grace", 2, 3000, datetime(2026, 1, 4, 11, 0), 1),
        ("east", 1, "Ada", 1, 2500, datetime(2026, 1, 2, 9, 0), 2),
        ("west", 4, "Sam", 1, 1000, datetime(2026, 1, 2, 13, 0), 1),
        ("west", 3, "Lin", 0, 0, None, 2),
    ]

