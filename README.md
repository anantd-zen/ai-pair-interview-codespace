# AI pair-interview Codespace

A reusable GitHub Codespaces environment for live Python or SQL interviews in
which the candidate may use AI. It includes VS Code Live Share, Copilot, a
customizable Pi installation, OpenRouter configuration, Python 3.12, DuckDB,
and two starter challenges.

The repository does **not** record Pi prompts, responses, or terminal activity.

## One-time setup

1. Push this repository to GitHub.
2. Create a short-lived, spending-limited OpenRouter key for an interview.
3. Make it available as the Codespaces secret `OPENROUTER_API_KEY`, restricted
   to this repository.

Anyone with a read/write terminal can potentially recover a secret inside the
Codespace. Use a unique, low-limit key and revoke it after the interview.

## Start an interview manually

1. On GitHub select **Code > Codespaces > Create codespace on main**.
2. Wait for `postCreateCommand` to install Python dependencies and Pi.
3. Start a Live Share session and approve the signed-in candidate.
4. Open a terminal, run `interview-pi`, and explicitly share that terminal
   read/write.
5. Select either the Python challenge in `CHALLENGE.md` or the SQL challenge in
   `sql/CHALLENGE.md`.

Terminals are not shared automatically. Copilot is installed, but a Live Share
guest does not inherit the host's Copilot identity or chat session.

## Start a session from PowerShell

The helper replaces the repository-scoped Codespaces secret and creates a fresh
Codespace:

```powershell
./scripts/new_interview.ps1 -OpenRouterKey 'sk-or-v1-...'
```

Or specify another repository:

```powershell
./scripts/new_interview.ps1 `
  -Repository 'OWNER/ai-pair-interview-codespace' `
  -OpenRouterKey 'sk-or-v1-...'
```

This intentionally accepts the key interactively as a parameter for the first
prototype. Avoid placing the command in shell history; a future control plane
should mint and revoke keys through OpenRouter's management API.

## Challenge commands

```bash
pytest -m python_challenge
python scripts/run_sql_challenge.py
pytest -m sql_challenge
interview-pi
```

The unused challenge is excluded by selecting the appropriate pytest marker.

## Custom Pi build

By default setup installs `@mariozechner/pi-coding-agent`. To use your own npm
package, set `PI_NPM_SPEC` as a Codespaces secret or update `scripts/setup.sh`.
Project-level behavior belongs in `AGENTS.md` and other Pi configuration files
you add to the repository.

## End an interview

Capture only the code or test results you are authorized to retain, delete the
Codespace, and revoke the interview-specific OpenRouter key.

