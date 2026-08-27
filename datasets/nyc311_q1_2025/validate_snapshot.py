"""Validate published NYC 311 snapshot invariants and checksums."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import duckdb


EXPECTED_REQUESTS = 884_765


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir", type=Path)
    args = parser.parse_args()
    root = args.snapshot_dir.resolve()
    requests = root / "nyc_311_requests_2025_q1.parquet"
    events = root / "nyc_311_events_2025_q1.parquet"
    manifest = json.loads((root / "snapshot_manifest.json").read_text(encoding="utf-8"))

    connection = duckdb.connect()
    request_stats = connection.execute(
        """
        SELECT
            count(*), count(DISTINCT request_id),
            min(created_at), max(created_at),
            count(*) FILTER (WHERE created_at < TIMESTAMP '2025-01-01'),
            count(*) FILTER (WHERE created_at >= TIMESTAMP '2025-04-01')
        FROM read_parquet(?)
        """,
        [str(requests)],
    ).fetchone()
    assert request_stats[0] == EXPECTED_REQUESTS
    assert request_stats[1] == EXPECTED_REQUESTS
    assert request_stats[4] == 0 and request_stats[5] == 0

    request_columns = {
        row[0]
        for row in connection.execute(
            "DESCRIBE SELECT * FROM read_parquet(?)", [str(requests)]
        ).fetchall()
    }
    forbidden = {
        "incident_address",
        "street_name",
        "cross_street_1",
        "cross_street_2",
        "intersection_street_1",
        "intersection_street_2",
        "landmark",
        "taxi_pick_up_location",
    }
    assert request_columns.isdisjoint(forbidden)

    event_stats = connection.execute(
        """
        SELECT
            count(*), count(DISTINCT event_id),
            count(*) FILTER (WHERE event_type = 'request_created'),
            count(*) FILTER (WHERE event_at IS NULL),
            count(*) FILTER (WHERE try_cast(payload AS JSON) IS NULL)
        FROM read_parquet(?)
        """,
        [str(events)],
    ).fetchone()
    assert event_stats[0] == event_stats[1]
    assert event_stats[2] == EXPECTED_REQUESTS
    assert event_stats[3] == 0
    assert event_stats[4] == 0
    connection.close()

    for filename, expected in manifest["statistics"]["files"].items():
        path = root / filename
        assert path.stat().st_size == expected["bytes"]
        assert sha256(path) == expected["sha256"]

    print(
        json.dumps(
            {
                "request_rows": request_stats[0],
                "event_rows": event_stats[0],
                "request_min": request_stats[2].isoformat(),
                "request_max": request_stats[3].isoformat(),
                "checksums": "ok",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

