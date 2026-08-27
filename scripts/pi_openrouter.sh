#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

key="${OPENROUTER_API_KEY:-${DEFAULT_OPENROUTER_API_KEY:-}}"
if [[ -z "$key" ]]; then
  echo 'No OpenRouter key is available.' >&2
  echo 'Add DEFAULT_OPENROUTER_API_KEY or OPENROUTER_API_KEY as a Codespaces secret.' >&2
  exit 1
fi

# Keep built-in OpenRouter and GitHub Copilot providers out of the interview
# picker. The custom provider reads this private variable from models.json.
export INTERVIEW_OPENROUTER_API_KEY="$key"
unset OPENROUTER_API_KEY
export PI_CODING_AGENT_DIR="$workspace_dir/.interview-work/pi-agent"

default_model="openrouter/free"
model="${PI_MODEL_OVERRIDE:-$default_model}"
if [[ ! "$model" =~ ^[A-Za-z0-9._:/-]+$ ]]; then
  echo 'PI_MODEL_OVERRIDE contains unsupported characters.' >&2
  exit 1
fi

real_pi="${PI_REAL_BINARY:-/usr/local/share/nvm/current/bin/pi-real}"
if [[ ! -x "$real_pi" ]]; then
  echo "The underlying Pi executable is missing: $real_pi" >&2
  echo 'Run bash scripts/setup.sh to repair the environment.' >&2
  exit 1
fi

exec "$real_pi" \
  --provider interview-openrouter \
  --model "$model" \
  --models "$model" \
  "$@"

