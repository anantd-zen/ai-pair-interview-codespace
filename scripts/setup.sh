#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_dir"

if [[ -z "${OPENROUTER_API_KEY:-${DEFAULT_OPENROUTER_API_KEY:-}}" ]]; then
  echo 'Missing DEFAULT_OPENROUTER_API_KEY Codespaces secret.' >&2
  echo 'See the root README: Fork -> Add the OpenRouter secret.' >&2
  exit 1
fi

uv sync --all-groups --frozen

pi_npm_spec="${PI_NPM_SPEC:-@mariozechner/pi-coding-agent}"
npm install --global "$pi_npm_spec"

pi_binary="$(command -v pi)"
pi_real="${pi_binary}-real"
pi_target="$(readlink "$pi_binary")"
if [[ -z "$pi_target" ]]; then
  echo "Expected npm's Pi executable to be a symbolic link: $pi_binary" >&2
  exit 1
fi

ln -sfn "$pi_target" "$pi_real"
ln -sfn "$workspace_dir/scripts/pi_openrouter.sh" "$pi_binary"

agent_dir="$workspace_dir/.interview-work/pi-agent"
mkdir -p "$agent_dir" "$HOME/.local/bin"
ln -sfn "$workspace_dir/.pi/models.json" "$agent_dir/models.json"
ln -sfn "$workspace_dir/scripts/pi_openrouter.sh" "$HOME/.local/bin/interview-pi"
ln -sfn "$workspace_dir/scripts/verify_environment.sh" "$HOME/.local/bin/verify-environment"

PI_CODING_AGENT_DIR="$agent_dir" "$pi_real" install npm:pi-web-access

snapshot_repo="${NYC311_RELEASE_REPOSITORY:-anantd-zen/ai-pair-interview-codespace}"
snapshot_tag="${NYC311_RELEASE_TAG:-nyc311-q1-2025}"
snapshot_dir="$workspace_dir/.interview-work/nyc311-q1-2025"
mkdir -p "$snapshot_dir"
gh release download "$snapshot_tag" \
  --repo "$snapshot_repo" \
  --pattern nyc_311_requests_2025_q1.parquet \
  --pattern nyc_311_events_2025_q1.parquet \
  --pattern snapshot_manifest.json \
  --dir "$snapshot_dir" \
  --clobber
.venv/bin/python datasets/nyc311_q1_2025/validate_snapshot.py "$snapshot_dir"

if [[ -f "$workspace_dir/challenge/setup.sh" ]]; then
  bash "$workspace_dir/challenge/setup.sh"
fi

bash scripts/verify_environment.sh

