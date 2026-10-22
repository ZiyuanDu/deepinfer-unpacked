# NPUGraph

> Ascend 系列 · M12 工程与实践 · 进阶
>
> 静态形状分桶与安全重放

[返回 Ascend 系列](../README.md) · [返回可执行教程](../../README.md)

本教程用一个最小示例说明：图捕获如何减少设备任务下发开销，以及 LLM Decode 面对动态 Batch 和 KV 长度时，为什么需要固定 shape、固定地址和形状分桶（shape bucketing）。

“分桶”表示把许多动态输入尺寸归入少量预设档位。例如实际 Batch 为 3 时，选择可容纳它的 Batch 档位 4。本文后续统一使用“形状分桶”或“档位”。

## 1. 学习目标与前置知识

完成本教程后，可以：

- 说明 CUDA Graph / NPUGraph 解决的性能问题；
- 根据实际 `(Batch, KV Length)` 选择静态图档位；
- 使用 `copy_()` 更新固定地址输入，并以 Eager 结果验证 Replay。

需要了解 PyTorch 张量、LLM 的 Prefill / Decode 阶段，并准备版本匹配的 CANN、驱动、固件、PyTorch 与 `torch_npu` 环境。

## 2. 从 Eager 执行到 CUDA Graph

PyTorch Eager 模式会在每次迭代中逐个下发算子。一个 Decode step 如果包含许多短算子，CPU 需要反复经过 Python、框架和驱动层发起 Kernel；设备可能在两次 Kernel 之间等待下一次下发。

```text
Eager，每个 step 都重复下发：
CPU  ──launch A──launch B──launch C──▶
NPU       A    空隙   B    空隙   C

Graph，首次捕获后整体重放：
首次：CPU ──capture(A → B → C)──▶ Graph
后续：CPU ──replay Graph────────▶ NPU: A → B → C
```

CUDA Graph 将一段 GPU 工作及其依赖关系记录成可重复启动的图。后续执行通过一次 Replay 提交整张图，减少逐算子参数准备和 Kernel Launch 开销。它主要改善 CPU 下发受限、计算结构重复的负载；设备计算本身已经占满时，收益通常较小。

Ascend NPUGraph 延续相同的 Capture / Replay 思路：

| 名称 | 含义 |
| --- | --- |
| Capture | 记录一次算子序列、依赖关系及其输入输出内存 |
| Replay | 使用捕获结果再次执行相同工作流 |
| 静态输入 | 捕获前创建、生命周期覆盖所有 Replay 的张量 |
| 形状分桶 | 将动态尺寸映射到有限个静态 shape 档位 |
| Padding | 用补齐数据填满档位中未被真实请求占用的部分 |

Capture 有一次性的预热、建图和内存开销。重复次数足够多时，这些成本才能被后续 Replay 摊薄。

## 3. 为什么 shape 和地址需要固定

### 3.1 shape 决定被捕获的执行计划

张量 shape 会影响矩阵尺寸、Attention 时间轴、Mask 大小、Kernel 启动参数和临时工作区。Capture 得到的是某一次执行的具体工作流；Replay 复用这套工作流时，需要继续满足捕获时的 shape 约束。

LLM Decode 中有两个持续变化的维度：

- 请求进入和完成会改变 Batch 大小 `B`；
- 每条序列逐 Token 增长，且长度不同，会改变 KV 长度 `L`。

直接按每一个 `(B, L)` 捕获会产生大量图。形状分桶把动态尺寸压缩为有限集合：

```text
实际请求 KV 长度：[17, 63, 9]
实际形状：(B=3, Lmax=63)
可用档位：B=[1, 2, 4, 8]，L=[16, 32, 64, 128]
选择图键：(B_bucket=4, L_bucket=64)
```

该图容纳 3 条真实请求和 1 条 Padding 行；KV 时间轴补齐到 64。实际尺寸超过最大档位时，规划器返回 Eager 路径。

### 3.2 Replay 读取捕获时的内存地址

图节点保存了捕获阶段使用的内存地址。新一轮输入需要写入同一块内存：

```python
static_input.zero_()
static_input[:actual_batch].copy_(dynamic_input)
graph.replay()
```

下面的赋值让 Python 变量指向新张量，已捕获的图仍持有旧地址：

```python
static_input = dynamic_input
```

因此静态输入和输出需要长期存活，每轮使用原地操作更新。示例额外检查 `data_ptr()`，用于发现 Replay 前地址意外变化。

## 4. 现有静态形状分桶的局限

资源与覆盖范围

- 图数量约为 `Batch 档位数 × KV 档位数`；档位增加会扩大捕获时间和常驻内存。
- 最大档位限制 Replay 覆盖范围，超长序列需要回退 Eager 或新增档位。

运行效率

- 较大的档位会执行更多 Padding 计算；较密的档位会保存更多图，需要按真实请求分布权衡。
- 每轮 `copy_()`、Mask/页表更新和同步都有成本；负载由设备计算主导时，图重放可能没有明显加速。
- Lazy Capture 会增加首次命中的延迟，预先捕获全部档位会增加启动时间和峰值显存。

正确性与兼容性

- Padding 行需要独立 scratch slot 和正确 Mask；复用真实 KV slot 会污染 Prefix Cache 或其他请求。
- 动态控制流、CPU 同步、数据相关 shape 和部分算子可能无法安全入图，具体能力取决于 CANN 与 `torch_npu` 版本。
- Capture 成功只说明工作流可以被记录；动态输入是否生效仍需逐轮与 Eager 输出对照。

本教程的线性层示例聚焦 shape、地址和 Replay 验证。接入真实 LLM Decode 时，还要验证 KV 页表、有效长度、Attention Mask、采样边界和 Padding 隔离。

## 5. 文件与代码流程

| 文件 | 作用 |
| --- | --- |
| `bucket_planner.py` | 生成档位，并把动态 KV 长度映射为静态图键 |
| `npugraph_replay_demo.py` | 完成预热、Capture、原地更新、Replay 和 Eager 对照 |
| `test_bucket_planner.py` | 覆盖分档、边界校验和 Eager fallback |

代码流程共三步：

1. `StaticBucketPlanner.plan()` 根据实际 Batch 数和最长 KV 长度选择 `(B_bucket, L_bucket)`。
2. 示例创建 Bucket shape 的静态输入，Eager 预热后捕获相同张量上的前向过程。
3. 每轮把新数据 `copy_()` 到静态输入，Replay 后仅截取真实请求行，并与 Eager 输出比较。

## 6. 运行与验证

CPU 上验证规划逻辑：

```bash
cd tutorials/ascend/npugraph
python -m unittest -v test_bucket_planner.py
```

Ascend 环境验证 Capture / Replay：

```bash
python npugraph_replay_demo.py \
  --batch-size 3 --batch-buckets 1,2,4,8 \
  --hidden-size 256 --replays 3
```

预期结果：每轮显示 `PASS`，最终显示 `actual batch=3, bucket=4`。这表示三次 Replay 均读取了本轮输入，输出与 Eager 路径在给定误差范围内一致。

同时记录软件栈与设备信息：

```bash
python -c "import torch, torch_npu; print(torch.__version__, torch_npu.__version__)"
npu-smi info
```

## 7. 常见问题与练习

**为什么每个输入都不能单独捕获一张图？** 频繁 Capture 会重复支付建图成本，图数量和常驻内存也会随动态 shape 快速增长。分桶让一张图覆盖一组相近 shape。

**为什么输出一致仍需测试多个 Replay？** 固定地址错误常表现为 Replay 持续读取第一次输入。每轮更换数据并与 Eager 对照，可以暴露陈旧输入问题。

**Bucket 越多越好吗？** 档位增多会降低 Padding 比例，同时提高捕获成本和内存占用。应根据线上 `(B, L)` 分布选择档位。

练习：修改 Batch 档位为 `(1, 4, 8)`，观察 `B=2` 的 Padding 比例；随后为规划器增加最大 Padding 比例限制，超过阈值时回退 Eager。

## 8. 小结与参考资料

动态图输入经过形状分桶得到有限个静态 shape；`copy_()` 在固定地址上更新数据；Eager 对照验证每次 Replay 的输入与输出。三者共同构成 NPUGraph Decode 适配的最小正确性闭环。

- [PyTorch：CUDA Graphs 与 CUDA 语义](https://docs.pytorch.org/docs/stable/notes/cuda.html#cuda-graphs)
- [NVIDIA：CUDA Graph 基础](https://docs.nvidia.com/dl-cuda-graph/latest/cuda-graph-basics/cuda-graph.html)
- [Ascend PyTorch：NPUGraph 开发说明](https://github.com/Ascend/pytorch/blob/master/docs/zh/developer_notes/npugraph.md)
- [Ascend PyTorch：版本兼容关系](https://github.com/Ascend/pytorch/blob/master/COMPATIBILITY.md)
