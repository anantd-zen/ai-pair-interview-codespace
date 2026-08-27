#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_dir"

python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'

pi_npm_spec="${PI_NPM_SPEC:-@mariozechner/pi-coding-agent}"
npm install --global "$pi_npm_spec"

mkdir -p .interview-work "$HOME/.local/bin"
ln -sfn "$workspace_dir/scripts/interview_pi.sh" "$HOME/.local/bin/interview-pi"
ln -sfn "$workspace_dir/scripts/verify_environment.sh" "$HOME/.local/bin/verify-environment"

bash scripts/verify_environment.sh

