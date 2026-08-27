#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${OPENROUTER_API_KEY:-}" && -n "${DEFAULT_OPENROUTER_API_KEY:-}" ]]; then
  export OPENROUTER_API_KEY="$DEFAULT_OPENROUTER_API_KEY"
fi

if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
  echo 'No OpenRouter key is available.' >&2
  echo 'Add DEFAULT_OPENROUTER_API_KEY or OPENROUTER_API_KEY as a Codespaces secret.' >&2
  exit 1
fi

default_model="openrouter/free"
model="${PI_MODEL_OVERRIDE:-$default_model}"
models="${PI_MODELS_OVERRIDE:-$default_model}"

if [[ ! "$model" =~ ^[A-Za-z0-9._:/-]+$ ]]; then
  echo 'PI_MODEL_OVERRIDE contains unsupported characters.' >&2
  exit 1
fi
if [[ ! "$models" =~ ^[A-Za-z0-9._:/,*-]+$ ]]; then
  echo 'PI_MODELS_OVERRIDE contains unsupported characters.' >&2
  exit 1
fi

real_pi="${PI_REAL_BINARY:-/usr/local/share/nvm/current/bin/pi-real}"
if [[ ! -x "$real_pi" ]]; then
  echo "The underlying Pi executable is missing: $real_pi" >&2
  echo 'Run bash scripts/setup.sh to repair the environment.' >&2
  exit 1
fi

exec "$real_pi" \
  --provider openrouter \
  --model "$model" \
  --models "$models" \
  "$@"

