"""Static bucket planning helpers for NPUGraph decode examples.

The module has no third-party dependency, so its boundary behavior can be
tested on a CPU-only machine before an Ascend environment is available.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


def _positive_sorted_unique(values: Iterable[int], *, name: str) -> tuple[int, ...]:
    result = tuple(sorted(set(values)))
    if not result or result[0] < 1:
        raise ValueError(f"{name} must contain positive integers")
    return result


def batch_buckets(max_batch_size: int) -> tuple[int, ...]:
    """Return practical decode batch buckets up to ``max_batch_size``."""
    if max_batch_size < 1:
        raise ValueError("max_batch_size must be positive")
    candidates = [1, 2, 4, 8]
    candidates.extend(range(16, max_batch_size + 1, 16))
    candidates.append(max_batch_size)
    return tuple(sorted({size for size in candidates if size <= max_batch_size}))


def kv_buckets(
    context_length: int,
    requested: Sequence[int] | None = None,
) -> tuple[int, ...]:
    """Return KV-length buckets, validating an optional explicit list."""
    if context_length < 1:
        raise ValueError("context_length must be positive")
    if requested is not None:
        sizes = _positive_sorted_unique(requested, name="requested KV buckets")
        if sizes[-1] > context_length:
            raise ValueError("a KV bucket exceeds context_length")
        return sizes
    defaults = (16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192)
    return tuple(sorted({size for size in defaults if size < context_length} | {context_length}))


def ceil_bucket(value: int, buckets: Sequence[int]) -> int | None:
    """Select the smallest bucket that can hold ``value``."""
    if value < 1:
        raise ValueError("value must be positive")
    return next((size for size in buckets if size >= value), None)


@dataclass(frozen=True)
class GraphKey:
    batch_size: int
    kv_length: int


class StaticBucketPlanner:
    """Map a dynamic decode step to a fixed ``(batch, KV length)`` graph key."""

    def __init__(
        self,
        *,
        max_batch_size: int,
        context_length: int,
        requested_kv_buckets: Sequence[int] | None = None,
    ) -> None:
        self.batch_sizes = batch_buckets(max_batch_size)
        self.kv_sizes = kv_buckets(context_length, requested_kv_buckets)

    def plan(self, kv_lengths: Sequence[int]) -> GraphKey | None:
        """Return ``None`` when the step must fall back to eager execution."""
        if not kv_lengths or any(length < 1 for length in kv_lengths):
            raise ValueError("kv_lengths must be a non-empty positive sequence")
        batch = ceil_bucket(len(kv_lengths), self.batch_sizes)
        kv_length = ceil_bucket(max(kv_lengths), self.kv_sizes)
        if batch is None or kv_length is None:
            return None
        return GraphKey(batch_size=batch, kv_length=kv_length)
