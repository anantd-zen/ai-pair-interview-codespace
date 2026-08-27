# Authoring a SQL pairing project

The environment includes DuckDB and the NYC 311 request/event snapshot.

Suggested layout:

```text
challenge/
├── README.md
├── AGENTS.md
├── setup.sh
└── workspace/
    ├── open.sql
    ├── work.sql
    ├── notes.md
    └── data/           # optional small local files
```

## Use NYC 311

Open the bundled dataset:

```bash
duckdb :memory: -init datasets/nyc311_q1_2025/open_snapshot.sql
```

Your challenge prompt can refer to:

```text
nyc_311_requests
nyc_311_events
```

The official dictionary, source limitations, privacy transformations, schema,
and challenge ideas live under `datasets/nyc311_q1_2025/`.

## Add a small dataset

Commit CSV, JSON, or small Parquet files under `challenge/workspace/data/`, then
create views in `challenge/workspace/open.sql`:

```sql
CREATE VIEW orders AS
SELECT * FROM read_csv_auto('challenge/workspace/data/orders.csv');
```

## Add a larger dataset

Publish immutable data as a release asset and download it from
`challenge/setup.sh`. Record:

- source URL and license;
- extraction window and query;
- retrieval timestamp;
- row counts and schema;
- SHA-256 checksums;
- transformations or privacy reductions.

Avoid depending on a mutable live API during the interview.

## Pairing formats

Useful SQL interviews include:

- open-ended data exploration;
- metric definition and validation;
- debugging a subtly wrong query;
- reconstructing state from events;
- designing a durable analytical model;
- improving correctness or performance;
- discussing missingness, censoring, duplicates, and late data.

The customer-revenue project under `examples/sql-customer-revenue/` shows a
small deterministic exercise. The NYC 311 data supports more realistic,
open-ended pairing.

