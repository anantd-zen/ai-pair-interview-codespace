# AI pair-interview Codespace

A reusable GitHub Codespaces environment for live Python or SQL interviews in
which the candidate may use AI.

The environment includes:

- Python 3.12 managed with `uv`;
- DuckDB as both a CLI and Python dependency;
- VS Code Live Share and GitHub Copilot;
- Pi configured for `openrouter/free` with `pi-web-access`;
- Python and SQL starter challenges;
- a reproducible NYC 311 Q1 2025 analytical snapshot.

The repository does **not** record Pi prompts, responses, or terminal activity.

## One-time setup

Add a repository-scoped Codespaces secret named
`DEFAULT_OPENROUTER_API_KEY`. Anyone with a read/write terminal can potentially
recover a secret inside the Codespace, so use an appropriately scoped key.

## Start an interview

1. On GitHub select **Code > Codespaces > Create codespace on main**.
2. Wait for setup to verify `uv`, DuckDB, Python, and Pi.
3. Start Live Share and approve the signed-in candidate.
4. From Live Share, create a new **read/write shared terminal**.
5. Type `pi` in that shared terminal.

Terminals are not shared automatically. A Live Share guest does not inherit the
host's private Copilot chat session.

## Available commands

```bash
uv --version
duckdb --version
pi
pytest -m python_challenge
python scripts/run_sql_challenge.py
pytest -m sql_challenge
```

## NYC 311 snapshot

The Q1 2025 snapshot contains 884,765 privacy-minimized service requests and
2,640,617 derived lifecycle events. The Parquet files are published as GitHub
Release assets and can be queried directly from DuckDB.

See [`datasets/nyc311_q1_2025/README.md`](datasets/nyc311_q1_2025/README.md)
for URLs, build instructions, the official data dictionary, schema notes, and
challenge ideas.

## Start a session from PowerShell

The helper uses `DEFAULT_OPENROUTER_API_KEY` unless an explicit per-interview
override is supplied:

```powershell
./scripts/new_interview.ps1
```

Optional override:

```powershell
./scripts/new_interview.ps1 -OpenRouterKey 'sk-or-v1-...'
```

## Custom Pi build

Setup currently installs `@mariozechner/pi-coding-agent`. Set `PI_NPM_SPEC` as
a Codespaces secret to install a customized package instead.

## End an interview

Capture only artifacts you are authorized to retain, delete the Codespace, and
revoke any interview-specific key.

