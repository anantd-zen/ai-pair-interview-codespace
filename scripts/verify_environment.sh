#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_dir"

printf 'Python: '
.venv/bin/python --version
printf 'Pi launcher: '
pi --version

if [[ -n "${OPENROUTER_API_KEY:-}" ]]; then
  echo 'OpenRouter key: per-interview override available (value not displayed)'
elif [[ -n "${DEFAULT_OPENROUTER_API_KEY:-}" ]]; then
  echo 'OpenRouter key: repository default available (value not displayed)'
else
  echo 'OpenRouter key: missing; add a Codespaces secret'
fi

echo 'Default provider: openrouter'
echo "Default model: ${PI_MODEL_OVERRIDE:-openrouter/free}"
echo 'Model picker: openrouter/free only'
echo 'Environment check complete.'

