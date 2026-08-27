#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_dir"

printf 'Python: '
.venv/bin/python --version
printf 'Pi: '
pi --version

if [[ -n "${OPENROUTER_API_KEY:-}" ]]; then
  echo 'OpenRouter key: available (value not displayed)'
else
  echo 'OpenRouter key: missing; add OPENROUTER_API_KEY as a Codespaces secret'
fi

echo 'Environment check complete.'

