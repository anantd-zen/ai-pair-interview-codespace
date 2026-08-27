# Authoring a Python pairing project

Create a self-contained project under `challenge/workspace/`.

Suggested layout:

```text
challenge/
├── README.md
├── AGENTS.md
├── setup.sh
└── workspace/
    ├── pyproject.toml
    ├── uv.lock
    ├── src/
    ├── sample_data/
    └── tests/          # optional
```

## Setup hook

When the project has its own `pyproject.toml`, customize `challenge/setup.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

uv sync --project challenge/workspace --all-groups --frozen
```

Commit the challenge's `uv.lock` so every interviewer receives the same
dependencies.

## Good pairing formats

The project does not need to be a function with static tests. Useful formats
include:

- diagnose and improve an incomplete service;
- add a small feature to an existing package;
- investigate a bug with logs or sample data;
- refactor a difficult module and explain tradeoffs;
- build a prototype around an external API;
- explore a LangChain or agent integration;
- review and harden AI-generated code.

Tests should support the intended conversation. They are optional, and they
must not be used as secret evaluator material when the candidate has shell
access.

## Pi context

Put challenge-specific information in `challenge/AGENTS.md`:

- architecture and important entry points;
- commands that are safe and useful;
- constraints the model should respect;
- how to verify work;
- domain terminology.

Do not encode a solution path or scoring rubric in candidate-visible Pi context.

The rate-limiter project under `examples/python-rate-limiter/` demonstrates an
isolated uv/Python project with tests, but it is only one possible format.

