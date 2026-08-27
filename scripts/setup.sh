#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_dir"

python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'

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

mkdir -p .interview-work "$HOME/.local/bin" "$HOME/.pi/agent"
ln -sfn "$workspace_dir/scripts/pi_openrouter.sh" "$HOME/.local/bin/interview-pi"
ln -sfn "$workspace_dir/scripts/verify_environment.sh" "$HOME/.local/bin/verify-environment"
ln -sfn "$workspace_dir/.pi/models.json" "$HOME/.pi/agent/models.json"

bash scripts/verify_environment.sh

