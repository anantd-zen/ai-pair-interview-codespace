# AI pairing-interview template

Fork this repository to create a self-contained Python, SQL, debugging, or
exploratory pairing interview in GitHub Codespaces. Interviewees may use the
bundled Pi coding agent through OpenRouter.

The environment includes:

- Python 3.12 and `uv`;
- DuckDB CLI and Python package;
- a populated NYC 311 analytical dataset;
- browser-based VS Code with Live Share;
- Pi configured for `openrouter/free` with `pi-web-access`;
- optional HTML session export for post-interview review.

The repository does **not** automatically record Pi prompts, terminal activity,
or the interview.

## Quick start: fork to interview

### 1. Fork this repository

Use GitHub's **Fork** button and create the fork under your account or team
organization. Customize only `challenge/` at first; the rest is reusable
infrastructure.

### 2. Add your OpenRouter Codespaces secret

Codespaces secrets are not copied into forks. Create or authorize this secret
for the fork:

```text
DEFAULT_OPENROUTER_API_KEY
```

Recommended personal-secret flow:

1. Open your GitHub profile **Settings**.
2. Select **Codespaces**.
3. Create `DEFAULT_OPENROUTER_API_KEY` with your OpenRouter key.
4. Grant the new fork access to the secret.

Alternatively, an administrator can add it under the fork's
**Settings → Secrets and variables → Codespaces**.

The devcontainer declares this as a recommended secret. When creating a
Codespace with **New with options**, GitHub prompts you to create or authorize
it if necessary.

Anyone with a read/write terminal can potentially recover environment secrets.
Use an appropriately scoped key and do not expose production credentials.

### 3. Customize the active challenge

Edit:

```text
challenge/README.md
challenge/AGENTS.md
challenge/workspace/
challenge/setup.sh       # optional
```

- `README.md` is the candidate-facing prompt.
- `AGENTS.md` gives Pi challenge-specific context.
- `workspace/` contains the code, data, notebooks, or SQL the candidate uses.
- `setup.sh` installs challenge-specific dependencies or prepares data.

See [Python challenge authoring](docs/authoring-python.md) and
[SQL challenge authoring](docs/authoring-sql.md). Finished reference exercises
live under `examples/`; they are not active interview content.

### 4. Create the Codespace

On the fork:

```text
Code → Codespaces → New with options
```

Confirm or enter `DEFAULT_OPENROUTER_API_KEY`, then create the Codespace from
`main`. Setup verifies the environment and downloads the NYC 311 snapshot.

You can also create a session from a local terminal:

```bash
./scripts/new_interview.sh
```

PowerShell:

```powershell
./scripts/new_interview.ps1
```

## Start Live Share

### Share the editor

1. Open the **Live Share** icon in the VS Code activity bar.
2. Click **Share**.
3. Copy the generated invitation link.
4. Send the **Live Share invitation**, not the Codespace URL, to the candidate.
5. Approve the participant when they join.
6. The candidate should sign in if they need read/write file access.

### Share a read/write terminal

Existing terminals remain private. Create a dedicated shared terminal:

1. Open the **Live Share** sidebar.
2. Find **Shared Terminals**.
3. Click **Share terminal** or `+`.
4. Select **Read/write**.
5. In the new shared terminal, run:

```bash
cd challenge
pi
```

If the terminal button is not visible:

```text
Ctrl+Shift+P → Live Share: Share Terminal → Read/write
```

Only the Live Share host can create the shared terminal. Read/write access gives
the candidate the same shell access as the interviewer.

## Bundled NYC 311 dataset

Codespace setup downloads and validates:

- 884,765 Q1 2025 service requests;
- 2,640,617 derived lifecycle events;
- the official NYC data dictionary and provenance manifest.

Open it with:

```bash
duckdb :memory: -init datasets/nyc311_q1_2025/open_snapshot.sql
```

DuckDB creates these views:

```text
nyc_311_requests
nyc_311_events
```

See [the dataset guide](datasets/nyc311_q1_2025/README.md),
[schema](datasets/nyc311_q1_2025/SCHEMA.md), and
[challenge ideas](datasets/nyc311_q1_2025/CHALLENGE_IDEAS.md).

Forks download the immutable release from this upstream repository by default.
Set `NYC311_RELEASE_REPOSITORY` or `NYC311_RELEASE_TAG` in `challenge/setup.sh`
before calling custom download logic if you publish a replacement snapshot.

## Customize Pi

The `pi` command automatically uses:

```text
provider: interview-openrouter
model:    openrouter/free
package:  pi-web-access
```

`openrouter/free` is a router, not a fixed model. OpenRouter chooses from free
models currently available and filters for capabilities required by a request,
such as tool calling. Output quality, latency, context limits, and upstream data
handling may vary between requests.

Common customization points:

- `challenge/AGENTS.md`: challenge-specific instructions and commands.
- `.pi/settings.json`: default provider/model and Pi settings.
- `.pi/models.json`: the custom OpenRouter provider entry.
- `PI_NPM_SPEC`: Codespaces secret or variable for a customized Pi package.
- `scripts/setup.sh`: install additional Pi packages.

See [Customizing Pi](docs/customizing-pi.md).

## Export a Pi session for review

At the start of the interview, name the session inside Pi:

```text
/name candidate-role-date
```

At the end, export it to HTML:

```text
/export ../.interview-work/review/candidate-role-date.html
```

Because Pi normally runs from `challenge/`, `../.interview-work/...` resolves to
the ignored review directory at the repository root.

If Pi has already exited, export the newest saved session with:

```bash
./scripts/export_latest_session.sh candidate-role-date
```

Download the HTML through VS Code Explorer before deleting the Codespace. Get
candidate consent and follow your team's retention policy. See
[Reviewing sessions](docs/reviewing-sessions.md).

## Security boundary

The candidate has a read/write shell. Do not include any material in this
repository or Codespace that the candidate must not see, including:

- solutions or hidden tests;
- rubrics and interviewer notes;
- production credentials or private datasets;
- previous candidates' exports.

Keep interviewer-only material in a separate restricted document or repository.
See [Security and privacy](docs/security-and-privacy.md).

## Template maintenance

From the repository root:

```bash
uv sync --all-groups --frozen
uv run pytest
uv run ruff check .
bash scripts/verify_environment.sh
```

The template baseline must remain healthy. Challenge-specific failures belong
inside `challenge/` or an example project, not in the root verification suite.

