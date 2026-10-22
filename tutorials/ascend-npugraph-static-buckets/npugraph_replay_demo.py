"""Minimal fixed-address NPUGraph capture and replay validation.

Run this file only in an environment where PyTorch, torch_npu, CANN, firmware,
and the driver use a supported version combination.
"""

from __future__ import annotations

import argparse

import torch

from bucket_planner import ceil_bucket


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=3)
    parser.add_argument("--batch-buckets", default="1,2,4,8")
    parser.add_argument("--hidden-size", type=int, default=256)
    parser.add_argument("--replays", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.batch_size < 1 or args.hidden_size < 1 or args.replays < 1:
        raise ValueError("batch-size, hidden-size and replays must be positive")

    try:
        import torch_npu
    except ImportError as exc:
        raise RuntimeError("this example requires torch_npu") from exc

    if not torch.npu.is_available():
        raise RuntimeError("Ascend NPU is unavailable")
    if not hasattr(torch_npu.npu, "NPUGraph") or not hasattr(torch_npu.npu, "graph"):
        raise RuntimeError("this torch_npu build does not expose NPUGraph APIs")

    buckets = tuple(sorted({int(value) for value in args.batch_buckets.split(",")}))
    if not buckets or buckets[0] < 1:
        raise ValueError("batch-buckets must contain positive integers")
    bucket = ceil_bucket(args.batch_size, buckets)
    if bucket is None:
        raise ValueError("batch-size exceeds the configured buckets")

    device = torch.device("npu:0")
    torch.manual_seed(7)
    model = torch.nn.Sequential(
        torch.nn.Linear(args.hidden_size, args.hidden_size, bias=False),
        torch.nn.ReLU(),
    ).to(device).eval()

    # Capture keeps these addresses. New data is staged with in-place copy_.
    static_input = torch.zeros((bucket, args.hidden_size), device=device)
    static_pointer = static_input.data_ptr()

    with torch.inference_mode():
        model(static_input)
        torch_npu.npu.synchronize()

        graph = torch_npu.npu.NPUGraph()
        with torch_npu.npu.graph(graph):
            static_output = model(static_input)
        torch_npu.npu.synchronize()

        for replay_index in range(args.replays):
            dynamic_input = torch.randn(
                (args.batch_size, args.hidden_size), device=device
            )
            eager_output = model(dynamic_input)

            static_input.zero_()
            static_input[: args.batch_size].copy_(dynamic_input)
            if static_input.data_ptr() != static_pointer:
                raise AssertionError("static input address changed before replay")

            graph.replay()
            torch_npu.npu.synchronize()
            torch.testing.assert_close(
                static_output[: args.batch_size], eager_output, rtol=1e-3, atol=1e-3
            )
            print(f"replay {replay_index + 1}: PASS")

    print(
        f"PASS: actual batch={args.batch_size}, bucket={bucket}, "
        f"hidden={args.hidden_size}, replays={args.replays}"
    )


if __name__ == "__main__":
    main()
