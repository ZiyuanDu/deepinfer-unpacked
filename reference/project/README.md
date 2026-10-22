# 项目与流程

本页说明本仓库的分工、产出流程与协作角色。更细的规范见 [交流规范](../CONTRIBUTING.md)、[Issue 规范](issues.md) 和 [PR 规范](pr.md)。

## 仓库分工

本仓库把「知识」和「项目流程」解耦为两部分：

| 路径 | 内容 |
| --- | --- |
| `docs/` | 知识本体：上手入门、教程正文、文档模板 |
| `reference/` | 项目流程：交流规范、Issue/PR 规范、模块表 |
| `tutorials/` | 可执行教程与实验 |

- 教程正文按模块编号组织，模块定义见 [DeepInfer 模块表](../MODULES.md)。
- 每个 Topic 遵循 [Topic 模板](../../docs/_templates/topic.md) 的结构。

## 产出流程

```text
Issue / Tracking  →  分支  →  PR  →  评审  →  Squash and merge  →  更新 checklist
```

1. **立项**：按 [Issue 规范](issues.md) 提交 Q&A / Confusion / Enhancement / Experiment，或在已有 Tracking issue 下认领一个 Topic。
2. **开发**：从 `main` 切出分支（命名见 [PR 规范](pr.md)），一个 PR 只处理一个 Topic。
3. **评审**：Module Owner 检查技术正确性，Chapter Editor 检查结构、术语与去重。
4. **合并**：至少 1 个 approval，使用 Squash and merge，合并后删除分支。
5. **收尾**：更新对应 Tracking issue 的 checklist，必要时把结论沉淀回现有文档。

## 角色

| 角色 | 职责 |
| --- | --- |
| Reader | 阅读文档，提出 Q&A / Confusion |
| Answerer | 回答提问，并把稳定结论沉淀为文档 |
| Experimenter | 跑可复现实验，产出报告 |
| Module Owner | 技术正确性与模块边界 |
| Chapter Editor | 章节结构、过渡、术语与去重 |
| Maintainer | triage、分支保护、里程碑管理 |

## 分支保护建议

- 禁止直接向 `main` 推送。
- 要求通过 PR 合并，且至少 1 个 approval。
