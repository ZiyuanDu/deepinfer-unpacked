# PR 规范

本页说明如何提交一个可评审、可合并的 PR。


## 基本规则

- 一个 PR 只处理一个 Topic，或一个明确的小修复。
- 内容 PR 关联一个 issue 或章节 Tracking issue。
- 不在 main 上直接提交；使用分支 + PR。

## 分支、标题与 Commit

分支示例：

```text
docs/m03-t02-continuous-batching
fix/m04-kv-index
experiment/m08-t03-sm100-benchmark
meta/pr-template
```

PR 标题示例：

```text
[M03-T02] 新增 continuous batching 章节
[M04] 修正 KV index 说明
[R00] 增加 PR 模板
```

Commit 示例：

```text
docs(M03-T02): add continuous batching section
fix(M04): correct KV index description
experiment(M08-T03): add SM100 benchmark report
```

## PR 描述

建议在 PR 描述中写清楚：

```markdown
## 关联
- Issue / Tracking: Part of #123
- Module: M03
- Topic: M03-T02

## 改了什么
...

## 为什么改
...


## 依据
- DeepInfer commit: ...
- 源码位置: ...
- 运行环境: ...

## 如何验证
...


```

## Topic 文件结构

新增 Topic 按 [Topic 模板](../../_templates/topic.md) 编写。至少包含：

- 学习目标
- 前置知识
- 核心问题
- 源码位置
- 概念解释
- 代码走读
- 图示
- 实验（可选）
- 常见误区
- 练习
- 小结
- 参考资料

## 评审与合并

- Module Owner 负责技术正确性和模块边界。
- Chapter Editor 负责章节结构、过渡、术语和去重。
- 至少需要 1 个 approval。
- 使用 Squash and merge，合并后删除分支。
- 合并后更新对应 Tracking issue 的 checklist。
- 建议开启分支保护：禁止直接 push main，要求 PR 和至少 1 个 approval。

## 多 PR 合成一章

多个 PR 将根据知识范围重新整理成为系统性的文档。
