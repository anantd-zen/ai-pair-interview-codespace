# Python challenge: sliding-window request limiter

Implement `SlidingWindowRateLimiter` in
`src/interview_challenge/rate_limiter.py`.

The limiter answers whether a request from a particular client should be
accepted. A client may have at most `limit` accepted requests in the trailing
`window_seconds` interval.

## Required behavior

- `allow(client_id, now)` returns `True` when the request is accepted.
- It returns `False` when the client is already at its limit.
- Rejected requests do not consume capacity.
- Requests exactly `window_seconds` old are expired.
- Clients are independent.
- `now` is caller supplied and monotonic for each client.
- Construction with a non-positive limit or window raises `ValueError`.

Aim for work proportional to the number of timestamps that expire, rather than
the total lifetime request count.

```bash
pytest -m python_challenge
```

You may use Pi by running `interview-pi` in the shared terminal.

