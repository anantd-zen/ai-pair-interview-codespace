#!/usr/bin/env bash
set -euo pipefail

# Optional challenge-specific setup hook.
#
# Python example:
#   uv sync --project challenge/workspace --all-groups
#
# Dataset example:
#   mkdir -p .interview-work/my-data
#   gh release download ...
#
# Leave this file as-is when the challenge needs no additional setup.

