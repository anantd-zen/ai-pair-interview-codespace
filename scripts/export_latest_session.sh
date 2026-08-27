#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
agent_dir="$workspace_dir/.interview-work/pi-agent"
session_dir="$agent_dir/sessions"
review_dir="$workspace_dir/.interview-work/review"
name="${1:-interview-$(date -u +'%Y%m%dT%H%M%SZ')}"

if [[ ! "$name" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo 'Export name may contain only letters, numbers, dots, underscores, and hyphens.' >&2
  exit 1
fi

latest="$(find "$session_dir" -type f -name '*.jsonl' -printf '%T@ %p\n' 2>/dev/null \
  | sort -nr | head -1 | cut -d' ' -f2-)"
if [[ -z "$latest" ]]; then
  echo 'No saved Pi session was found.' >&2
  exit 1
fi

mkdir -p "$review_dir"
output="$review_dir/$name.html"
PI_CODING_AGENT_DIR="$agent_dir" \
  /usr/local/share/nvm/current/bin/pi-real --export "$latest" "$output"
echo "$output"

