# Security and privacy boundaries

## Candidate shell access

A read/write Live Share terminal gives the candidate the same command-line
access as the host. Treat every file, environment variable, Git ref, and local
artifact in the Codespace as candidate-visible.

Do not include:

- solutions, hidden tests, rubrics, or interviewer notes;
- production API keys or cloud credentials;
- private customer or employee data;
- previous candidate sessions;
- credentials embedded in code or Git history.

Live Share file exclusions are useful for presentation but are not a security
boundary when the candidate has terminal access.

## Model data handling

`openrouter/free` may route different requests to different upstream providers.
Do not send confidential source code, personal data, or secrets. Recheck
OpenRouter and upstream provider terms before using the environment for a new
kind of interview material.

## Dataset privacy

The bundled NYC 311 snapshot omits exact address fields and rounds coordinates.
Its documentation describes remaining source and interpretation limitations.

## Session exports

HTML exports are not committed and are stored under `.interview-work/`. Obtain
candidate consent, control access, and delete them according to your retention
policy.

