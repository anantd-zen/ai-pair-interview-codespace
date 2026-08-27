# Customizing the bundled Pi agent

Typing `pi` uses the repository's wrapper and isolated interview configuration.

## Default model

The default is `openrouter/free`. It dynamically routes to a currently
available free model that supports the request's required features. It is not a
fixed or deterministic model.

Use a different model only when the challenge requires it and you have verified
availability, cost, tool support, and data-handling terms.

## Context hierarchy

- Root `AGENTS.md` describes template-wide behavior.
- `challenge/AGENTS.md` describes the active challenge.
- Pi loads context by walking from the current directory upward, so start Pi
  from `challenge/`.

Use `.pi/APPEND_SYSTEM.md` when you need to append repository-wide system
instructions. Avoid replacing the full system prompt unless necessary.

## Pi packages

`pi-web-access` is installed during Codespace setup. Add another reviewed
package in `scripts/setup.sh`:

```bash
PI_CODING_AGENT_DIR="$agent_dir" "$pi_real" install npm:package-name
```

Pi packages execute with the same filesystem and shell access as Pi. Review
third-party code and pin versions when reproducibility matters.

## Customized Pi distribution

Set the Codespaces variable or secret `PI_NPM_SPEC` to an npm/Git source that is
compatible with the expected Pi CLI. Otherwise setup uses the package pinned in
`scripts/setup.sh`.

## OpenRouter key

The wrapper reads `OPENROUTER_API_KEY` first, then
`DEFAULT_OPENROUTER_API_KEY`. The key is passed to Pi through its official
`--api-key` option.

Anyone with read/write terminal access can inspect credentials available to the
Codespace. Use a key whose scope and spending controls are appropriate for an
interview environment.

