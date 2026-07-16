# Workflow Map 模板

Grill 阶段结束后使用本模板。workflow map 是实现前最关键的门禁。

## 目录

- [规则](#规则)
- [精简 Workflow Map](#精简-workflow-map)
- [给用户的确认话术](#给用户的确认话术)
- [完成标准](#完成标准)

## 规则

workflow map 未经展示和确认前，不要编写目标 `SKILL.md`。

## 精简 Workflow Map

```markdown
# [Skill Name] Workflow Map

## 目的
[这个 Skill 要稳定让 agent 完成什么。]

## Leading Words
- [word 1]
- [word 2]

## 触发
- 模式：model-invoked / user-invoked
- 应该触发于：
  - [真实用户说法]
  - [真实用户说法]
- 不应该触发于：
  - [near miss]

## 工作流

### Step 1: [名称]
- 目的：
- 管控级别：L1/L2/L3/L4/L5/L6
- 输入：
- 必需 refs：
- 必需 scripts/tools：
- 人机介入点：
- 输出：
- Contract：
- Completion criterion：
- 常见失败：

### Step 2: [名称]
- 目的：
- 管控级别：
- 输入：
- 必需 refs：
- 必需 scripts/tools：
- 人机介入点：
- 输出：
- Contract：
- Completion criterion：
- 常见失败：

## 分支
- 如果 [条件]，读取 [reference] 并执行 [branch workflow]。
- 如果 [条件]，使用 [script/tool] 并用 [check] 验证。

## 人机介入点
| 介入点 | 时机 | 用户看到什么 | 用户选择/提供什么 | 保存到哪里 |
|---|---|---|---|---|

## 资源
### references/
- [file]：[何时读取]

### scripts/
- [file]：[何时运行]

### assets/
- [file/folder]：[何时使用]

## 验证计划
- 步骤级检查：
- 端到端 eval prompts：
- 人类 review 形式：
- 五种失败模式扫描：

## 持续迭代机制
- Memory Audit：
- Skill 升级路径：
- 旧内容删除/失效规则：
```

## 给用户的确认话术

使用简洁确认：

```text
这是我整理出的 workflow map。请重点检查：
1. 步骤顺序是否正确？
2. 是否漏掉人类确认点？
3. 是否漏掉应该脚本化的重复操作？
4. 是否漏掉或过度加入了 reference？

在这张 map 被确认或修正前，我不会开始实现 Skill。
```

## 完成标准

workflow map 完成需要满足：

- 每一步都有具体输出
- 每一步都有 completion criterion
- 每个必要的人机介入点都已定位
- 每个 reference/script/asset 都有存在理由
- 已初步检查五种失败模式不会被 workflow 设计放大
- 已规划目标 Skill 的持续迭代机制
- 用户已经确认 workflow，或已给出修正
