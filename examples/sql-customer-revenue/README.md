# Example: SQL customer revenue report

This is an **authoring example**, not the active interview challenge.

It demonstrates a small deterministic DuckDB project with schema, seed data, a
candidate query file, and optional tests. Open-ended SQL challenges can instead
use the bundled NYC 311 snapshot without a fixed expected result.

## Run the example

```bash
cd examples/sql-customer-revenue
uv sync --all-groups
uv run python run_query.py
uv run pytest
```

The candidate-facing example prompt is in `sql/CHALLENGE.md`.

