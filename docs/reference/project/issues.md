# Issue 规范

本仓库围绕 DeepInfer 开展源码研读、文档整理和实验补充。DeepInfer 本身的 bug 请提交至 [上游仓库](https://github.com/deepseek-ai/DeepInfer/issues)。

## 四种 issue

| 类型 | 定义 | 完成标志 |
| --- | --- | --- |
| Q&A | 明确的问题 | 回答被确认；必要时沉淀为文档 |
| Confusion | 现有文档中矛盾、术语不清或逻辑跳跃的问题 | 困惑点被解释；若暴露文档缺陷，转 Enhancement |
| Enhancement | 现有文档、代码、教程、翻译需要被明确改进 | PR 合并，或方案被明确接受/拒绝 |
| Experiment | 有可验证假设，需要跑数据或性能实验 | 报告可复现、结论明确 |

- 针对仓库文档/教程的大段逻辑错误，选择 Enhancement，并且写明错误原因。
- 错别字、失效链接、小段修正，请直接提交 PR，不必新增 issue。
- Experiment 请写明硬件环境、假设、指标和预期结果；如果还没有想清楚，可以先提交 Q&A/Confusion。

## 提交前准备

1. 选择类型：Q&A / Confusion / Enhancement / Experiment。
2. 选择对应[模块](../modules.md)；如果不确定，请选择你认为最接近的相关模块。
3. 定义问题：请用一段话写明具体的疑问或改进点。
4. 位置与版本：写明对应源仓库的文件或者本仓库的文档，对于概念问题可写 N/A。
5. 背景与尝试：说明自己已有的思考与探索。

## 提交方式

[Issue 表单](https://github.com/ZiyuanDu/deepinfer-unpacked/issues/new/choose)

标题格式：`[类型] 模块 一句话`

每个 issue 只提交一个问题；多个问题请拆开。

## 提交之后

- 维护者会做 triage，可能请你进一步补充相关信息。
- 问题解决后，我们会尽量把结论总结到现有文档中。
- 这是志愿者项目，不承诺立即回复。

## 示例

### 示例一：环境配置

**正确示例**

标题：`[Q&A] M12 如何在 8 卡 H100 上配置 DeepInfer？`

- **类型**：Q&A
- **模块**：M12 工程与实践
- **问题定义**：如何在 8 卡 H100 上配置 DeepInfer？需要说明驱动、CUDA、依赖和启动步骤；能跑通 `examples/offline_inference.py` 即算解决。
- **位置与版本**：`README.md` 的构建章节、`build.sh`；commit `9bd9cf2`
- **背景与已尝试**：已阅读 README 的 build 步骤，但尚未成功在 8 卡 H100 上跑通现有模块。

**错误示例**

> 8卡H100怎么配DeepInfer，急

问题：没有类型、模块、版本和范围，也没有说明已经尝试过什么。

### 示例二：概念困惑

**正确示例**

标题：`[Confusion] M03 ZOS 的异步调度机制是什么？`

- **类型**：Confusion
- **模块**：M03 调度与执行
- **问题定义**：ZOS 的异步调度机制是什么？它在请求生命周期中负责哪一段？
- **位置与版本**：`csrc/engine/zos.cpp`；commit `9bd9cf2`
- **背景与已尝试**：在源码中看到 `zos.cpp` 和 `schedule_mtp_varlen.py`，目前理解为一种异步调度机制，不确定它与 continuous batching 的关系。

**错误示例**

> 各位大佬，我不是很清楚 ZOS 的异步调度机制是什么，求解释

问题：没有模块和源码位置，没有说明当前理解，也没有说明什么算解决。

## 通用规范

通用交流规范见 [CONTRIBUTING](..CONTRIBUTING.md#基本规则)。

提交代码或文档改动见 [PR 规范](pr.md)。
