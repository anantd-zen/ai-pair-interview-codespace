import pytest

from interview_challenge import SlidingWindowRateLimiter


pytestmark = pytest.mark.python_challenge


def test_accepts_until_limit_then_rejects() -> None:
    limiter = SlidingWindowRateLimiter(limit=3, window_seconds=10)
    assert limiter.allow("alice", 0)
    assert limiter.allow("alice", 1)
    assert limiter.allow("alice", 2)
    assert not limiter.allow("alice", 3)


def test_timestamp_at_window_boundary_is_expired() -> None:
    limiter = SlidingWindowRateLimiter(limit=2, window_seconds=5)
    assert limiter.allow("alice", 10)
    assert limiter.allow("alice", 11)
    assert limiter.allow("alice", 15)
    assert not limiter.allow("alice", 15.5)
    assert limiter.allow("alice", 16)


def test_rejected_requests_do_not_consume_capacity() -> None:
    limiter = SlidingWindowRateLimiter(limit=1, window_seconds=10)
    assert limiter.allow("alice", 0)
    assert not limiter.allow("alice", 1)
    assert not limiter.allow("alice", 9.9)
    assert limiter.allow("alice", 10)


def test_clients_are_independent() -> None:
    limiter = SlidingWindowRateLimiter(limit=1, window_seconds=10)
    assert limiter.allow("alice", 0)
    assert limiter.allow("bob", 0)
    assert not limiter.allow("alice", 1)
    assert not limiter.allow("bob", 1)


@pytest.mark.parametrize(
    ("limit", "window_seconds"),
    [(0, 1), (-1, 1), (1, 0), (1, -0.1)],
)
def test_rejects_non_positive_configuration(limit: int, window_seconds: float) -> None:
    with pytest.raises(ValueError):
        SlidingWindowRateLimiter(limit=limit, window_seconds=window_seconds)

