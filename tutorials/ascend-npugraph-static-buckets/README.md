# M12 · Ascend NPUGraph 静态 Bucket 与安全重放

## 学习目标

完成本教程后，可以解释动态 Decode 为何需要静态 Bucket，并能验证 NPUGraph 重放是否读取了本轮输入。

## 前置知识

- PyTorch 张量、Eager 执行与 NPU Stream
- LLM 的 Prefill / Decode 阶段
- 已匹配的 CANN、驱动、固件、PyTorch 与 `torch_npu` 环境

## 核心问题

Decode 的 Batch 大小和 KV 长度会随请求变化；NPUGraph 重放要求形状、内存地址和执行路径保持稳定。解决链路为：

```text
动态 (B, L) → 向上选择 (B_bucket, L_bucket) → padding 写入静态输入
             → copy_ 保持 data_ptr → replay → 只返回真实请求行
```

形状超过最大 Bucket 时返回 Eager 路径。每个 Bucket 对应一张图，档位数量会直接增加捕获时间与显存占用。

## 源码位置

- `bucket_planner.py`：纯 Python Bucket 规划与 Eager fallback 判定
- `npugraph_replay_demo.py`：固定地址输入、捕获、更新和重放
- `test_bucket_planner.py`：边界与分档测试

## 概念解释

### Bucket 键

LLM Decode 通常以 `(Batch Bucket, KV Length Bucket)` 作为图键：Batch Bucket 固定并发维度，KV Bucket 固定 Attention 的时间轴。实际值向上取整，例如 `B=3, Lmax=63` 映射到 `(4, 64)`。

### 固定地址输入

图捕获记录张量地址。每轮输入必须写入捕获时创建的静态张量：

```python
static_input.zero_()
static_input[:actual_batch].copy_(dynamic_input)
graph.replay()
```

重新赋值 `static_input = dynamic_input` 会改变 Python 变量指向，图仍读取捕获时的旧地址。

### Padding 隔离

真实推理引擎还需要为 padding 行准备独立 scratch slot。padding 行写入真实 KV slot 会污染 Prefix Cache 或其他请求。本教程用无状态的线性层演示地址与形状约束；接入 KV Cache 时必须额外验证 scratch slot 隔离、Mask 和页表边界。

## 代码走读

1. `StaticBucketPlanner.plan()` 使用实际 Batch 数和最长 KV 长度选择图键；无可用档位时返回 `None`。
2. 示例先创建 Bucket 形状的 `static_input`，执行一次 Eager warmup，再捕获相同张量上的前向过程。
3. 每轮生成新输入，通过 `copy_()` 原地更新；重放结果与 Eager 输出逐项比较。

## 实验

CPU 上验证规划逻辑：

```bash
cd tutorials/ascend-npugraph-static-buckets
python -m unittest -v test_bucket_planner.py
```

Ascend 环境验证捕获和重放：

```bash
python npugraph_replay_demo.py \
  --batch-size 3 --batch-buckets 1,2,4,8 \
  --hidden-size 256 --replays 3
```

成功标准：每轮显示 `PASS`，最终输出 `actual batch=3, bucket=4`。同时记录以下环境信息，避免把不同软件栈的结果直接比较：

```bash
python -c "import torch, torch_npu; print(torch.__version__, torch_npu.__version__)"
npu-smi info
```

## 常见误区

- 捕获成功仅证明算子可以入图；Eager/Replay 输出一致性才能验证动态输入是否生效。
- 首次捕获成本和热态 Replay 延迟属于不同指标，应分开记录。
- Bucket 越密，padding 浪费越少；图数量、捕获时间和显存占用会同步增加。

## 练习

1. 将 Batch Bucket 改为 `(1, 4, 8)`，观察 `B=2` 的 padding 比例。
2. 为 planner 增加最大 padding 比例限制，超过限制时回退 Eager。
3. 将示例线性层替换为实际 Decode 子图，补充 KV scratch slot 与 Mask 测试。

## 小结

NPUGraph 的动态 Decode 适配依赖三个不变量：静态形状、静态地址、稳定执行路径。Bucket 负责静态形状，`copy_()` 负责静态地址，Eager 对照负责验证重放正确性。

## 参考资料

- [Ascend PyTorch：NPUGraph 开发说明](https://github.com/Ascend/pytorch/blob/master/docs/zh/developer_notes/npugraph.md)
- [Ascend PyTorch：版本兼容关系](https://github.com/Ascend/pytorch/blob/master/COMPATIBILITY.md)
