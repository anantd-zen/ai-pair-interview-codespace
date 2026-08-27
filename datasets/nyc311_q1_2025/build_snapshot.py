"""Build a reproducible, privacy-minimized NYC 311 Q1 2025 snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

import duckdb


DATASET_ID = "erm2-nwe9"
RESOURCE_URL = f"https://data.cityofnewyork.us/resource/{DATASET_ID}"
METADATA_URL = f"https://data.cityofnewyork.us/api/views/{DATASET_ID}"
DICTIONARY_ASSET_ID = "c5cc6926-45bb-4af3-8aab-0ee6a29bcf4d"
DICTIONARY_NAME = "311_ServiceRequest_2020-present_DataDictionary_Updated_2025.xlsx"
DICTIONARY_URL = (
    f"https://data.cityofnewyork.us/api/views/{DATASET_ID}/files/"
    f"{DICTIONARY_ASSET_ID}?download=true"
)
WINDOW_START = "2025-01-01T00:00:00"
WINDOW_END = "2025-04-01T00:00:00"
PAGE_SIZE = 50_000

FIELDS = [
    "unique_key",
    "created_date",
    "closed_date",
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "descriptor_2",
    "location_type",
    "incident_zip",
    "city",
    "facility_type",
    "status",
    "due_date",
    "resolution_description",
    "resolution_action_updated_date",
    "community_board",
    "council_district",
    "police_precinct",
    "bbl",
    "borough",
    "open_data_channel_type",
    "park_facility_name",
    "park_borough",
    "vehicle_type",
    "taxi_company_borough",
    "bridge_highway_name",
    "latitude",
    "longitude",
]


def api_url(format_name: str, **params: object) -> str:
    return f"{RESOURCE_URL}.{format_name}?{urllib.parse.urlencode(params)}"


def request_bytes(url: str, *, attempts: int = 6, timeout: int = 300) -> bytes:
    headers = {"User-Agent": "ai-pair-interview-nyc311-snapshot/1.0"}
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(
                urllib.request.Request(url, headers=headers), timeout=timeout
            ) as response:
                return response.read()
        except (TimeoutError, urllib.error.HTTPError, urllib.error.URLError) as error:
            if attempt == attempts:
                raise
            delay = min(30, 2 ** (attempt - 1))
            print(f"Request failed ({error}); retrying in {delay}s", file=sys.stderr)
            time.sleep(delay)
    raise AssertionError("unreachable")


def download(url: str, destination: Path, *, resume: bool = True) -> None:
    if resume and destination.exists() and destination.stat().st_size > 0:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_bytes(request_bytes(url))
    os.replace(temporary, destination)


def source_count() -> int:
    where = f"created_date >= '{WINDOW_START}' AND created_date < '{WINDOW_END}'"
    url = api_url("json", **{"$select": "count(*) as row_count", "$where": where})
    payload = json.loads(request_bytes(url))
    return int(payload[0]["row_count"])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sql_path(path: Path) -> str:
    return path.resolve().as_posix().replace("'", "''")


def download_pages(raw_dir: Path, expected_rows: int, *, resume: bool) -> None:
    where = f"created_date >= '{WINDOW_START}' AND created_date < '{WINDOW_END}'"
    pages = math.ceil(expected_rows / PAGE_SIZE)
    for page in range(pages):
        offset = page * PAGE_SIZE
        destination = raw_dir / f"page-{page:03d}.csv"
        url = api_url(
            "csv",
            **{
                "$select": ",".join(FIELDS),
                "$where": where,
                "$order": "created_date,unique_key",
                "$limit": PAGE_SIZE,
                "$offset": offset,
            },
        )
        print(f"[{page + 1}/{pages}] {destination.name}")
        download(url, destination, resume=resume)


def build_parquet(raw_dir: Path, output_dir: Path, expected_rows: int) -> dict[str, object]:
    request_path = output_dir / "nyc_311_requests_2025_q1.parquet"
    event_path = output_dir / "nyc_311_events_2025_q1.parquet"
    raw_glob = sql_path(raw_dir / "page-*.csv")

    connection = duckdb.connect()
    connection.execute(
        f"""
        CREATE TEMP VIEW source_rows AS
        SELECT *
        FROM read_csv(
            '{raw_glob}',
            header = true,
            all_varchar = true,
            union_by_name = true,
            null_padding = true
        )
        """
    )
    actual_rows = connection.execute("SELECT count(*) FROM source_rows").fetchone()[0]
    if actual_rows != expected_rows:
        raise RuntimeError(f"Expected {expected_rows:,} source rows, found {actual_rows:,}")

    connection.execute(
        """
        CREATE TEMP TABLE requests AS
        SELECT
            unique_key AS request_id,
            created_date::TIMESTAMP AS created_at,
            try_cast(nullif(closed_date, '') AS TIMESTAMP) AS closed_at,
            nullif(agency, '') AS agency,
            nullif(agency_name, '') AS agency_name,
            nullif(complaint_type, '') AS problem,
            nullif(descriptor, '') AS problem_detail,
            nullif(descriptor_2, '') AS additional_details,
            nullif(location_type, '') AS location_type,
            nullif(incident_zip, '') AS incident_zip,
            nullif(city, '') AS city,
            nullif(facility_type, '') AS facility_type,
            nullif(status, '') AS status,
            try_cast(nullif(due_date, '') AS TIMESTAMP) AS due_at,
            nullif(resolution_description, '') AS resolution_description,
            try_cast(nullif(resolution_action_updated_date, '') AS TIMESTAMP)
                AS resolution_updated_at,
            nullif(community_board, '') AS community_board,
            nullif(council_district, '') AS council_district,
            nullif(police_precinct, '') AS police_precinct,
            nullif(bbl, '') AS bbl,
            nullif(borough, '') AS borough,
            nullif(open_data_channel_type, '') AS channel,
            nullif(park_facility_name, '') AS park_facility_name,
            nullif(park_borough, '') AS park_borough,
            nullif(vehicle_type, '') AS vehicle_type,
            nullif(taxi_company_borough, '') AS taxi_company_borough,
            nullif(bridge_highway_name, '') AS bridge_highway_name,
            round(try_cast(nullif(latitude, '') AS DOUBLE), 3) AS latitude_approx,
            round(try_cast(nullif(longitude, '') AS DOUBLE), 3) AS longitude_approx,
            CASE
                WHEN closed_at IS NOT NULL
                THEN date_diff('second', created_at, closed_at) / 3600.0
            END AS resolution_hours,
            CASE
                WHEN closed_at IS NOT NULL AND due_at IS NOT NULL
                THEN closed_at <= due_at
            END AS closed_by_due_date
        FROM source_rows
        """
    )

    unique_rows = connection.execute("SELECT count(DISTINCT request_id) FROM requests").fetchone()[0]
    if unique_rows != expected_rows:
        raise RuntimeError(f"Expected unique request IDs; found {unique_rows:,} distinct")

    connection.execute(
        f"""
        COPY (
            SELECT * FROM requests ORDER BY created_at, request_id
        ) TO '{sql_path(request_path)}'
        (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000)
        """
    )

    connection.execute(
        """
        CREATE TEMP TABLE events AS
        SELECT
            request_id || ':created' AS event_id,
            request_id,
            'request_created' AS event_type,
            created_at AS event_at,
            agency,
            problem,
            problem_detail,
            borough,
            'Open' AS status_after,
            channel,
            to_json(struct_pack(
                location_type := location_type,
                incident_zip := incident_zip,
                council_district := council_district,
                police_precinct := police_precinct,
                latitude_approx := latitude_approx,
                longitude_approx := longitude_approx
            )) AS payload
        FROM requests

        UNION ALL

        SELECT
            request_id || ':resolution_updated', request_id,
            'resolution_updated', resolution_updated_at,
            agency, problem, problem_detail, borough, status, channel,
            to_json(struct_pack(
                resolution_description := resolution_description,
                due_at := due_at,
                closed_by_due_date := closed_by_due_date
            ))
        FROM requests
        WHERE resolution_updated_at IS NOT NULL

        UNION ALL

        SELECT
            request_id || ':closed', request_id,
            'request_closed', closed_at,
            agency, problem, problem_detail, borough, 'Closed', channel,
            to_json(struct_pack(
                resolution_hours := resolution_hours,
                resolution_description := resolution_description,
                closed_by_due_date := closed_by_due_date
            ))
        FROM requests
        WHERE closed_at IS NOT NULL
        """
    )
    connection.execute(
        f"""
        COPY (
            SELECT * FROM events ORDER BY event_at, event_id
        ) TO '{sql_path(event_path)}'
        (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000)
        """
    )

    statistics = connection.execute(
        """
        SELECT
            count(*) AS request_rows,
            min(created_at) AS min_created_at,
            max(created_at) AS max_created_at,
            count(*) FILTER (WHERE closed_at IS NOT NULL) AS closed_requests,
            count(*) FILTER (WHERE resolution_updated_at IS NOT NULL)
                AS resolution_updated_requests,
            count(*) FILTER (WHERE latitude_approx IS NOT NULL) AS geocoded_requests,
            count(DISTINCT agency) AS agencies,
            count(DISTINCT problem) AS problems
        FROM requests
        """
    ).fetchone()
    event_rows = connection.execute("SELECT count(*) FROM events").fetchone()[0]
    event_types = dict(
        connection.execute(
            "SELECT event_type, count(*) FROM events GROUP BY event_type ORDER BY event_type"
        ).fetchall()
    )
    connection.close()

    return {
        "request_rows": statistics[0],
        "min_created_at": statistics[1].isoformat(),
        "max_created_at": statistics[2].isoformat(),
        "closed_requests": statistics[3],
        "resolution_updated_requests": statistics[4],
        "geocoded_requests": statistics[5],
        "agencies": statistics[6],
        "problems": statistics[7],
        "event_rows": event_rows,
        "event_types": event_types,
        "files": {
            request_path.name: {
                "bytes": request_path.stat().st_size,
                "sha256": sha256(request_path),
            },
            event_path.name: {
                "bytes": event_path.stat().st_size,
                "sha256": sha256(event_path),
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    work_dir = args.work_dir.resolve()
    raw_dir = work_dir / "raw"
    reference_dir = output_dir / "reference"
    output_dir.mkdir(parents=True, exist_ok=True)
    reference_dir.mkdir(parents=True, exist_ok=True)

    count_before = source_count()
    print(f"Source rows at start: {count_before:,}")
    download_pages(raw_dir, count_before, resume=not args.no_resume)

    download(METADATA_URL, reference_dir / "source_metadata.json", resume=False)
    download(DICTIONARY_URL, reference_dir / DICTIONARY_NAME, resume=False)

    statistics = build_parquet(raw_dir, output_dir, count_before)
    count_after = source_count()
    if count_after != count_before:
        raise RuntimeError(
            f"Source changed during extraction: {count_before:,} -> {count_after:,}; rerun"
        )

    manifest = {
        "snapshot": "nyc311-q1-2025",
        "generated_at": datetime.now(UTC).isoformat(),
        "source": {
            "dataset_id": DATASET_ID,
            "metadata_url": METADATA_URL,
            "resource_url": RESOURCE_URL,
            "dictionary_url": DICTIONARY_URL,
            "window_start_inclusive": WINDOW_START,
            "window_end_exclusive": WINDOW_END,
            "selected_fields": FIELDS,
            "source_rows": count_before,
        },
        "privacy": {
            "omitted": [
                "incident_address",
                "street_name",
                "cross_street_1",
                "cross_street_2",
                "intersection_street_1",
                "intersection_street_2",
                "landmark",
                "taxi_pick_up_location",
            ],
            "coordinate_rounding_decimal_places": 3,
        },
        "statistics": statistics,
    }
    (output_dir / "snapshot_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

