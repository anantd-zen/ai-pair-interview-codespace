#!/usr/bin/env bash
set -euo pipefail

repository="${1:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}"
branch="${2:-main}"
machine="${CODESPACE_MACHINE:-basicLinux32gb}"

if [[ -z "$repository" ]]; then
  echo 'Could not determine the repository. Pass OWNER/REPO as the first argument.' >&2
  exit 1
fi

echo "Creating a fresh Codespace for $repository..."
gh codespace create \
  --repo "$repository" \
  --branch "$branch" \
  --machine "$machine" \
  --default-permissions \
  --idle-timeout 30m

