# Example: Python sliding-window rate limiter

This is an **authoring example**, not the active interview challenge.

It demonstrates a conventional Python exercise with a candidate-facing prompt,
an isolated `pyproject.toml`, source package, and tests. Copy the pattern into
`challenge/workspace/` only when static tests support the interview you want to
run.

## Example prompt

Implement `SlidingWindowRateLimiter` in
`src/interview_challenge/rate_limiter.py`.

A client may have at most `limit` accepted requests in the trailing
`window_seconds` interval.

- Rejected requests do not consume capacity.
- Requests exactly `window_seconds` old are expired.
- Clients are independent.
- Caller-supplied timestamps are monotonic per client.
- Non-positive limits or windows raise `ValueError`.

## Run the example

```bash
cd examples/python-rate-limiter
uv sync --all-groups
uv run pytest
```

