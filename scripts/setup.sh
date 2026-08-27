#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_dir"

uv venv --allow-existing --python python .venv
uv pip install --python .venv/bin/python -e '.[dev]'

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

bash scripts/verify_environment.sh

