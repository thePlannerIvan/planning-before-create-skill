# 管控级别与 Contracts

把 workflow map 转成 Skill 设计时使用本文件。

## 管控级别

选择“足以防住失败模式的最弱管控”。

| 级别 | 模式 | 适用场景 | 主要防线 |
|---|---|---|---|
| L1 | Prompt 约束 | 简单、低风险步骤 | 清晰步骤指令 |
| L2 | 文件关隘 | 步骤之间传递产物 | 必需输出文件 |
| L3 | 外部 hook/script | 验证可以确定性执行 | 脚本判定通过/失败 |
| L4 | 拆分 Agent | 复杂工作需要专注 legwork | 隐藏后续步骤 |
| L5 | 合约模式 | 高风险质量门槛 | Evaluator 检查断言 |
| L6 | 脚本编排 Agent | 长流程、固定、可重复 | 脚本控制顺序 |

## 决策矩阵

```text
                低灵活度                         高灵活度
高复杂度        L6 脚本编排                       L4 拆分 Agent + L5 合约
中复杂度        L3 hooks + L2 文件关隘             L4 拆分 Agent
低复杂度        L2 文件关隘                       L1 Prompt 约束
```

把人类介入也纳入判断：

- 如果继续前必须由人决定方向，加入 checkpoint gate。
- 如果人类 review 会改变下游行为，把反馈保存进 contract。
- 如果人类反馈复杂且主观，用 review artifact，而不是在聊天里堆长文。

## Step Contract

每个非平凡步骤都应该产出 contract 文件或等价的结构化交接。

最小字段：

```json
{
  "step": "step-id",
  "outputs": [],
  "checks_passed": [],
  "warnings": [],
  "human_decision": null,
  "next_step_context": "",
  "open_questions": []
}
```

## Contract 规则

- 上一步的输出 contract，就是下一步的输入 contract。
- 下一步开始前必须检查缺失输出、warnings 和必需的人类决定。
- 如果前置条件缺失，停止并报告缺失项。
- 不要依赖对话记忆传递会影响下游工作的状态。

## 资源放置

| 内容 | 放到哪里 | 原因 |
|---|---|---|
| 所有分支都需要的核心 workflow | `SKILL.md` | 触发后总是需要 |
| 每一步详细指令 | `references/workflow/` | 只在该步骤需要 |
| 领域知识和 schema | `references/domain/` | 分支特定知识 |
| Contract 模板 | `references/contracts/` | 保持交接一致 |
| 确定性检查 | `scripts/validate/` | 避免模型自评 |
| 重复转换 | `scripts/transform/` | 避免反复写代码 |
| 固定编排 | `scripts/orchestrate/` | 强制执行顺序 |
| 模板和可复用素材 | `assets/` | 用于产出 |

## 文件关隘模式

```markdown
### Step N
- 开始前，确认 `work/contract_N-1.json` 存在。
- 读取 `work/contract_N-1.json` 和必需输出。
- 产出 `work/step_N_output.md`。
- 产出 `work/contract_N.json`。
- 如果 contract 无法完成，停止。
```

## Contract 完成标准

Contract 完成需要满足：

- 所有列出的 outputs 都存在
- checks 是具体的，不是模糊的
- warnings 明确写出
- 必需的人类决定已记录
- next-step context 简短且可执行
