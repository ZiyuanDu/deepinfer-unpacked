from __future__ import annotations

import unittest

from bucket_planner import (
    GraphKey,
    StaticBucketPlanner,
    batch_buckets,
    ceil_bucket,
    kv_buckets,
)


class BucketPlannerTest(unittest.TestCase):
    def test_batch_buckets_keep_non_power_of_two_limit(self) -> None:
        self.assertEqual(batch_buckets(6), (1, 2, 4, 6))

    def test_default_kv_buckets_include_context_limit(self) -> None:
        self.assertEqual(kv_buckets(100), (16, 32, 64, 100))

    def test_requested_kv_buckets_are_sorted_and_unique(self) -> None:
        self.assertEqual(kv_buckets(128, [128, 32, 32]), (32, 128))

    def test_ceil_bucket(self) -> None:
        self.assertEqual(ceil_bucket(3, (1, 2, 4, 8)), 4)
        self.assertIsNone(ceil_bucket(9, (1, 2, 4, 8)))

    def test_plan_uses_batch_and_longest_kv_length(self) -> None:
        planner = StaticBucketPlanner(max_batch_size=8, context_length=128)
        self.assertEqual(planner.plan([17, 63, 9]), GraphKey(4, 64))

    def test_plan_falls_back_beyond_largest_kv_bucket(self) -> None:
        planner = StaticBucketPlanner(
            max_batch_size=4,
            context_length=128,
            requested_kv_buckets=[16, 64],
        )
        self.assertIsNone(planner.plan([65]))

    def test_invalid_values_fail_early(self) -> None:
        with self.assertRaises(ValueError):
            batch_buckets(0)
        with self.assertRaises(ValueError):
            kv_buckets(64, [16, 128])
        with self.assertRaises(ValueError):
            StaticBucketPlanner(max_batch_size=4, context_length=64).plan([])


if __name__ == "__main__":
    unittest.main()
