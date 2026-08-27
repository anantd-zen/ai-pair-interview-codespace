from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]


def test_template_has_active_challenge() -> None:
    assert (ROOT / "challenge" / "README.md").is_file()
    assert (ROOT / "challenge" / "AGENTS.md").is_file()


def test_duckdb_is_available() -> None:
    assert duckdb.sql("SELECT 40 + 2").fetchone() == (42,)

