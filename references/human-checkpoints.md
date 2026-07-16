# 人机介入点

workflow 需要人类方向、review、纠偏或知识输入时，使用本文件。

## 原则

人类介入是 workflow 的一部分，不是自动化失败。要设计用户何时进入、看到什么、如何反馈，以及反馈如何改变下一步。

模型倾向于做太多之后才问。强流程 Skill 应该在高价值决策点更早停下来。

## 人类介入类型

- **方向介入**：用户选择策略路径或优先级。
- **质量介入**：用户 review 中间产物是否足够好。
- **知识介入**：用户补充缺失背景、示例、凭据、文件或判断。
- **批准介入**：高成本或不可逆操作前获得确认。

## 交互设计规则

- 展示精简摘要，不展示原始日志。
- 尽量只问一个聚焦问题。
- 方向选择使用 2-3 个互斥选项。
- 给出推荐选项和一句 tradeoff。
- 复杂反馈使用 review artifact。
- 反馈保存到下一步 contract，不只留在对话里。

## Checkpoint 模板

```markdown
## Human Checkpoint: [名称]

When:
- [Step N 之后、Step N+1 之前]

Why:
- [这个人类介入防住什么风险]

Show:
- [不超过 5 行]
- [关键差异或决策]
- [必要时链接 review artifact]

Ask:
- [一个聚焦问题或 2-3 个选项]

Save feedback to:
- `contract_N.human_decision`
- `contract_N.constraints_for_next_step`
- 可选 memory candidate
```

## Review Artifact 选择

使用能支撑好反馈的最轻量形式：

| 场景 | 形式 |
|---|---|
| 简单方向选择 | 聊天中的短选项 |
| 中等 review | Markdown checklist |
| 多个样例 | 表格 |
| 输出对比 | HTML review page |
| 迭代 evals | 可导出 `feedback.json` 的 HTML 页面 |

如果需要一个轻量 HTML review 页面，可复制 `assets/review-page-template.html` 并替换其中的审阅内容。

## 坏 Checkpoint 的味道

- 让用户确认一大段无结构内容。
- 一次问多个互不相关的问题。
- 隐藏真实 tradeoff。
- 把用户反馈只当聊天记录，不当结构化状态。
- 本该中途决定的方向，拖到最后才问。
