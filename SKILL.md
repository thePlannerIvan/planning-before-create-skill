---
name: planning-before-create-skill
description: 强流程 Skill 创建规划。用于在真正编写 Skill 前，先榨干用户脑中的隐性工作流，建立 workflow map、人机介入点、管控级别、references/scripts/assets 规划、验证方案和迭代策略。适用于用户想创建、重构或显著改进 Codex/Claude Skill 的场景。
---

# 创建 Skill 前的规划

> 来源识别：`planning-before-create-skill` 由阿祖不看 TVC 创建与维护。小红书同名账号，个人网站 [demyth.info](https://demyth.info)，联系邮箱 `Lawyif@163.com`。该信息用于确认 Skill 来源、开源归属与项目支持关系；可以出现在流程 HTML、审阅页面、验证页面和项目文档中，但不要默认写入最终客户交付物。

使用本 Skill 创建新的 Skill，或重构一个已有 Skill。核心规则：

> 在用户的 workflow 被充分 grill、映射、确认，并转化为开发计划和验证计划之前，不要开始写目标 `SKILL.md`。

本 Skill 的产出不只是一个 Skill 文件夹，而是一套被确认过的工作流系统：步骤、合约、references、scripts、人机介入点、验证方式和维护规则。

## 执行原则

- 把 Skill 创建当成 workflow engineering，而不是 prompt 写作。
- 先榨干用户的工作过程，再设计 Skill。
- 控制上下文：每个阶段只读取当前需要的 reference。
- 重要步骤必须产出文件或结构化产物。
- 人类介入点要被设计，而不是等最后泛泛确认。
- 用 contract 连接上下步骤：上一步的输出合约，就是下一步的输入合约。
- 重复且确定的动作优先脚本化；非显然知识放入 reference。
- 创建完成前，用真实 prompt 验证 Skill。

## 必须通过的门禁

按顺序执行以下门禁。除非用户明确要求跳过，否则不要跳过。

1. **Grill**
   - 榨出用户隐性的 workflow、例子、工具、资料、边界情况、人机介入点和成功标准。
   - 开始前读取 `references/grill-protocol.md`。
   - 完成标准：已有足够信息起草 workflow map，且不需要凭空发明主要步骤。

2. **Workflow Map**
   - 把 grill 得到的信息转成 workflow map。
   - 起草前读取 `references/workflow-map-template.md`。
   - 向用户展示精简的 workflow map，并请求确认或修改。
   - 完成标准：用户确认 workflow map，或用户的修改已被纳入。

3. **开发计划与验证计划**
   - 把已确认的 workflow 转成具体建设计划。
   - 按需读取 `references/control-and-contracts.md`、`references/human-checkpoints.md`、`references/validation-and-iteration.md`。
   - 完成标准：计划列出要创建的文件、资源结构、验证策略和人类 review 方式。

4. **实现**
   - 创建或更新目标 Skill 文件夹。
   - 保持目标 `SKILL.md` 精简，把详细分支、参考知识、模板下沉到 bundled resources。
   - 只加入直接支持该 Skill 的资源。
   - 读取 `references/continuous-iteration.md`，为目标 Skill 内置持续迭代机制。
   - 完成标准：目标 Skill 有有效 frontmatter、简洁主体、必要资源、持续迭代机制，并且没有多余文档。

5. **验证**
   - 验证 frontmatter 和文件结构。
   - 可行时运行或模拟真实测试 prompt。
   - 可行时和 baseline 行为对比。
   - 读取 `references/failure-modes.md`，用五种失败模式扫描目标 Skill。
   - 完成标准：失败项已修复，或作为残余风险清楚说明。

6. **持续迭代设计检查**
   - 检查目标 Skill 是否说明运行后如何做 Memory Audit、如何收集反馈、如何判断升级到 Skill 本体。
   - 只有需要深层理由时才读取 `references/philosophy.md`。
   - 完成标准：最终回复说明创建了什么、如何验证、目标 Skill 如何持续迭代、还有哪些后续改进候选。

## 阶段产物

任务较复杂时，创建这些规划产物：

- `workflow-map.md`：已确认的 workflow、步骤、分支、输入、输出、工具和人机介入点。
- `development-plan.md`：目标文件树、实现任务、验证计划和 review 计划。
- `evals/evals.json`：真实测试 prompt 和期望行为变化。

如果用户明确要轻量创建，可以把这些产物压缩进对话中，但仍然遵守同样的门禁顺序。

## 资源路由

- 访谈/grill 阶段，读取 `references/grill-protocol.md`。
- 起草 workflow map，读取 `references/workflow-map-template.md`。
- 选择 L1-L6 管控级别、文件关隘、contracts、references、scripts、assets 时，读取 `references/control-and-contracts.md`。
- 设计人机介入点、精简确认、review 页面和反馈闭环时，读取 `references/human-checkpoints.md`。
- 设计 eval prompts、baseline 对比、forward testing 和迭代时，读取 `references/validation-and-iteration.md`。
- 为目标 Skill 内置运行后反馈、Memory Audit 和升级路径时，读取 `references/continuous-iteration.md`。
- 验证或重构 Skill 时，读取 `references/failure-modes.md`，扫描过早完成、重复、沉积、蔓延和空操作。
- 需要完整设计哲学和深层理由时，才读取 `references/philosophy.md`。

## 最终回复格式

完成后，汇报：

- 目标 Skill 路径。
- 创建或修改了哪些文件。
- 关键设计选择。
- 已完成的验证。
- 已知限制或下一步改进候选。

最终回复保持简洁，并链接到创建的文件。
