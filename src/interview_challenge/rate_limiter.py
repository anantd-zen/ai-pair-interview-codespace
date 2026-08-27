"""Sliding-window rate limiter challenge."""


class SlidingWindowRateLimiter:
    """Allow a bounded number of requests per client in a trailing window."""

    def __init__(self, limit: int, window_seconds: float) -> None:
        """Create a limiter. See ``CHALLENGE.md`` for required behavior."""
        raise NotImplementedError

    def allow(self, client_id: str, now: float) -> bool:
        """Return whether the request is accepted."""
        raise NotImplementedError

