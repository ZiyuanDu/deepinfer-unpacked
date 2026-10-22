# DeepInfer Unpacked

这是一个共同建设的 [DeepInfer](https://github.com/deepseek-ai/DeepInfer) 源码研读项目。

我们希望汇集数千名学习者和开发者，共同梳理 DeepInfer 的系统架构。  
我们将 DeepSeek 研究成果整理成一套有清晰前置知识、可以持续维护的中英文教程。

> [点这里开始学习](docs/) | [点这里参与项目](./reference/README.md)

## 从这里开始

在这个仓库中，你有以下四种角色：

| **角色** | 你想做什么 | 推荐入口 |
| --- | --- | --- |
| **阅读者** | 新手入门，从零开始学习 | [阅读路线](docs/start/01-reading-path.md) |
| **提问者** | 针对 DeepInfer 中的某项技术提出清晰明确的问题或提交改进 | [参与方式](./reference/README.md) |
| **解答者** | 回答提问者提出的问题 | [参与方式](./reference/README.md) |
| **实验者** | 针对 DeepInfer 的某项功能进行性能测试，或者在 DeepInfer 的基础上适配更多模型架构 | [参与方式](./reference/README.md) |


## 探究问题

本项目围绕 DeepInfer 的公开实现建立知识体系，逐步覆盖以下内容。

| 内容 | 主要问题 |
| --- | --- |
| 前置理论知识 | 补充 DeepInfer 需要的最小前置知识 |
| 前置代码知识 | 补充 DeepInfer 需要的最小动手能力 |
| DeepInfer 架构 | 掌握其系统架构与请求主线，包括但不限于调度与执行、缓存与资源管理、模型结构、算子与内核、多模态与视觉、并行与通信、高级机制、验证与性能分析等 |
| DeepInfer 代码补充 | 根据当前 DeepInfer 架构，补充一至两个合理的开源模型加入其中 |
| 外置知识 | 掌握 DeepInfer 所使用的 FlashMLA、DeepGEMM、DeepEP、DeepSelect、TileKernels、TileLang 等最小闭包 |


## 模块划分

| 编码 | 模块 | 定位 |
| --- | --- | --- |
| M00 | 整体架构 | DeepInfer 的目标、分层、请求主线与模块关系 |
| M01 | 前置理论 | Attention、MoE、KV cache、量化、推理指标 |
| M02 | 前置代码 | Python/PyTorch、CUDA、TileLang、C++、NCCL |
| M03 | 调度与执行 | 请求生命周期、batching、prefill/decode、异步执行 |
| M04 | 缓存与资源管理 | KV cache、block、显存、SWA、shared memory |
| M05 | 模型结构 | 模型加载、DeepSeek 模型、decoder、层定义 |
| M06 | 算子与内核 | TileLang、CUDA/C++/Ascend kernel、融合算子 |
| M07 | 多模态与视觉 | 视觉编码、图像预处理、multimodal tokens |
| M08 | 并行与通信 | TP/DP/EP/CP、DeepEP、EPLB、拓扑 |
| M09 | 高级机制 | 结构化输出、投机/验证、确定性、batch invariance |
| M10 | 验证与性能 | AIME/GPQA/HLE、benchmark、PPL、profiling |
| M11 | 外置组件 | FlashMLA、DeepGEMM、DeepEP、DeepSelect、TileLang |
| M12 | 工程与实践 | 构建、NVIDIA/Ascend、部署、模型适配 |

详细源码映射见 [模块表](reference/MODULES.md)。



## 仓库结构

| 路径 | 内容 |
| --- | --- |
| `docs/start/` | 上手与入门 |
| `docs/chapters/` | DeepInfer 教程正文 |
| `reference/` | 本项目流程 |
| `docs/_templates/` | 文档模板 |
| `tutorials/` | 可执行教程与实验 |
| `tutorials/ascend/` | Ascend 系列教程 |


## 当前进展

项目处于启动阶段，首阶段目标是完成对于 DeepInfer 架构的完整拆解。

可执行示例见 [tutorials](tutorials/README.md)。

## 杜子源有话说


期待各位的参与！
