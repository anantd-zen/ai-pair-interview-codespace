#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_dir"

if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
  echo 'OPENROUTER_API_KEY is not set.' >&2
  exit 1
fi

if ! command -v pi >/dev/null 2>&1; then
  echo 'Pi is not installed. Run bash scripts/setup.sh.' >&2
  exit 1
fi

model="${PI_MODEL:-anthropic/claude-sonnet-4}"
if [[ ! "$model" =~ ^[A-Za-z0-9._:/-]+$ ]]; then
  echo 'PI_MODEL contains unsupported characters.' >&2
  exit 1
fi

echo "Starting Pi session with model: $model"
echo 'Do not type secrets into the shared session.'
exec pi --provider openrouter --model "$model"

