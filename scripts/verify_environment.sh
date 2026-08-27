#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_dir"

printf 'uv: '
uv --version
printf 'DuckDB CLI: '
duckdb --version
printf 'Python: '
.venv/bin/python --version
printf 'Python DuckDB: '
.venv/bin/python -c 'import duckdb; print(duckdb.__version__)'
printf 'Pi launcher: '
pi --version

if [[ -n "${OPENROUTER_API_KEY:-}" ]]; then
  echo 'OpenRouter key: per-interview override available (value not displayed)'
elif [[ -n "${DEFAULT_OPENROUTER_API_KEY:-}" ]]; then
  echo 'OpenRouter key: repository default available (value not displayed)'
else
  echo 'OpenRouter key: missing; add a Codespaces secret'
fi

snapshot_dir="$workspace_dir/.interview-work/nyc311-q1-2025"
if [[ -f "$snapshot_dir/nyc_311_requests_2025_q1.parquet" \
   && -f "$snapshot_dir/nyc_311_events_2025_q1.parquet" ]]; then
  echo 'NYC 311 snapshot: available and checksum-validated'
else
  echo 'NYC 311 snapshot: missing; rerun bash scripts/setup.sh'
fi

echo 'Default provider: interview-openrouter'
echo 'Default model: openrouter/free'
echo 'Environment check complete.'

