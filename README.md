# DeepInfer Unpacked

这是一个共同建设的 [DeepInfer](https://github.com/deepseek-ai/DeepInfer) 源码研读项目。

我们希望汇集数千名学习者和开发者，共同梳理 DeepInfer 的系统架构，将研究成果整理成一套有清晰前置知识、经过同行评审、可以持续维护的中英文教材。

## 从这里开始

在这个仓库中，你有以下四种角色：

| **角色** | 你想做什么 | 推荐入口 |
| --- | --- | --- |
| **阅读者** | 新手入门，从零开始学习 | [阅读路线](docs/start/reading-path.md) |
| **提问者** | 针对 DeepInfer 中的某项技术提出清晰明确的问题或提交改进 | [参与方式](CONTRIBUTING.md) |
| **解答者** | 回答提问者提出的问题|[参与方式]()|
| **实验者** |针对 DeepInfer 的某项功能进行性能测试，或者在 DeepInfer 的基础上适配更多模型架构|[参与方式]()|


## 探究问题

本项目围绕 DeepInfer 的公开实现建立知识体系，逐步覆盖以下内容。

| 内容 | 主要问题 |
| --- | --- |
| 前置理论知识 | 补充 DeepInfer 需要的最小前置知识 |
| 前置代码知识 | 补充 DeepInfer 需要的最小动手能力 |
| DeepInfer 架构| 掌握其系统架构与请求主线，包括但不限于调度与执行、缓存与资源管理、模型与算子、并行与通信、高级机制、验证与性能分析等 |
| DeepInfer 代码补充| 根据当前 DeepInfer 架构，补充一至两个合理的开源框架加入其中 |
| 外置知识 |掌握 DeepInfer 所使用的 FlashMLA、DeepGEMM、DeepEP、DeepSelect、TileKernels、TileLang 等最小闭包|


## 知识如何组织

本项目核心采用文档驱动的协作方式。将明确各章节的学习目标和前置知识，再拆分研究问题。

核心通过 issues 模块进行管理，

- 2026-10-21 管理方式为：label 分为四个模块，Q&A、Confusion、Enhancement、Experiment。分别对应提问、疑惑、补充以及实验。所有的模块都需要通过提交 PR 的方式进行参与。




## 仓库结构

| 路径 | 内容 |
| --- | --- |
| [`docs/start/`](docs/start/) | 项目范围、阅读路线与章节大纲 |
| [`docs/prerequisites/`](docs/prerequisites/) | 张量、推理、生命周期、分布式和异步执行等基础知识卡 |
| [`docs/chapters/`](docs/chapters/) | 按知识依赖组织的正文章节与试读稿 |
| [`docs/reference/`](docs/reference/) | 源码、术语与外部库索引 |
| [`docs/community/`](docs/community/) | 参与方式与同行评审规范 |
| [`curriculum/`](curriculum/) | 章节目标、前置关系和问题编号 |
| [`labs/`](labs/) | 概念演示与最小参考实现 |
| [`evidence/`](evidence/) | 关键结论的证据说明与运行记录 |
| [`templates/`](templates/) | 章节、评审记录与证据模板 |
| [`issues/seed-tasks.md`](issues/seed-tasks.md) | 首批研究问题草案 |
| [`upstream.lock.yaml`](upstream.lock.yaml) | 研读使用的上游基准版本与依赖记录 |
| [`.github/`](.github/) | Issue 表单、PR 模板和基础检查流程 |

维护者可以进一步阅读[架构与启动方案](ARCHITECTURE.md)和[维护分工](GOVERNANCE.md)。

## 如何阅读

首次阅读建议沿一条请求主线展开。

1. 阅读[范围与系统地图](docs/start/scope.md)，认识模块与研究边界。
2. 阅读[一次请求的生命周期](docs/chapters/request-lifecycle.md)，建立整体执行过程。
3. 阅读[请求与序列表示](docs/chapters/request-representation.md)，区分关键对象和字段。
4. 阅读[引擎迭代与 Worker](docs/chapters/engine-step.md)，追踪一轮执行中的交接。
5. 阅读[输出生命周期](docs/chapters/output-lifetime.md)，理解资源归属和跨轮使用的约束。

遇到陌生概念时，按章节链接补充前置知识。已有基础的读者可以从[源码索引](docs/reference/source-map.md)进入专题，再核对对应章节的前置要求。

阅读文档和多数源码研究无需运行完整 DeepInfer。没有目标硬件，也可以参与调用追踪、手工推演、CPU 参考实现、已有运行记录分析和文档试读。


## 当前进展

项目处于启动阶段，首阶段目标是完成对于 DeepInfer 架构的完整专题。

## 杜子源有话说

> 

期待各位的参与！

