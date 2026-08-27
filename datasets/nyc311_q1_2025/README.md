# NYC 311 Q1 2025 interview snapshot

This snapshot contains NYC 311 service requests created from 2025-01-01 through
2025-03-31. It is designed for SQL pairing exercises in DuckDB.

## Published files

- `nyc_311_requests_2025_q1.parquet`: one row per service request.
- `nyc_311_events_2025_q1.parquet`: a derived lifecycle-event projection.
- `snapshot_manifest.json`: provenance, counts, privacy decisions, sizes, and SHA-256 hashes.
- `reference/`: the official NYC XLSX dictionary and Socrata metadata captured with the snapshot.

The Parquet files are private GitHub Release assets. Codespace setup downloads
and checksum-validates them once using the authenticated GitHub CLI.

## Open in DuckDB

From the repository root:

```bash
duckdb -init datasets/nyc311_q1_2025/open_snapshot.sql
```

The initialization script creates:

- `nyc_311_requests`
- `nyc_311_events`

Example:

```sql
SELECT borough, count(*) AS requests
FROM nyc_311_requests
GROUP BY borough
ORDER BY requests DESC;
```

Files live under `.interview-work/nyc311-q1-2025/`, which is intentionally
ignored by Git.

## Build locally

```bash
uv run --with duckdb==1.5.5 \
  datasets/nyc311_q1_2025/build_snapshot.py \
  --work-dir .interview-work/nyc311-q1-2025-build \
  --output-dir .interview-work/nyc311-q1-2025-build/dist
```

Downloads are paginated and resumable. The build fails if the source count
changes while extraction is in progress.

## Important interpretation caveat

The source is a daily-updated current-record dataset, not a true NYC change log.
The event file derives `request_created`, `resolution_updated`, and
`request_closed` events from timestamps on each source row. It must not be
interpreted as a complete history of every status mutation.

Complaint volume is also not an objective measurement of underlying city
conditions: it measures reported complaints and is affected by awareness,
access, behavior, and channel usage.

Source: https://data.cityofnewyork.us/resource/erm2-nwe9

