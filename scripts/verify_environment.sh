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

echo 'Default provider: interview-openrouter'
echo 'Default model: openrouter/free'
echo 'Environment check complete.'

