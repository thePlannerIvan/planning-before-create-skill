# 验证与迭代

开发计划和完成验收时完整读取。

## 原则

验证必须在实现前设计。一个 Skill 只有在真实失败模式上改变模型行为，才算变好。文件存在、Schema 通过和关键词命中不能证明语义任务已经完成。

## 分开两类验证

### 工程验证

- Frontmatter 与目录结构；
- Script 是否可执行并返回可诊断错误；
- Contract 的 Producer、Consumer 与 Validator 是否一致；
- Dispatcher 是否正确保存、恢复和披露当前 Stage；
- Review 是否能展示、保存、绑定版本并回传；
- Active 路径是否有孤儿文件。

### 语义验证

- 模型是否理解整个任务和当前 Stage；
- 是否使用了判断框架而不是机械填字段；
- 脚本是否让模型更轻，而不是制造额外回执；
- 人是否只在不可替代的决策点介入；
- 输出是否在真实任务中更准确、完整和有用；
- Validator 绿色时是否仍可能出现低质量结果。

不能用工程验证冒充语义 Forward Test。

## 先验证路线选择

验证不只检查 System 路线是否完整，还要检查它是否被滥用：

- Patch 请求应直接局部修改，不启动 Grill 或 Workflow Map；
- Lean 请求应有精简设计确认，但不生成 System 级文件和 Contract；
- System 请求应先还原隐性方法，完成 Workflow Map 和用户确认后再实现。

## 开发计划（`development-plan.md`）

确有跨会话、多人交接或用户独立审阅需求时，把下面几项写成一份计划；否则在对话里确认即可：

- 要创建、修改、删除或归档的文件；
- 代表性 Eval，以及需要时与旧版的 Baseline 对照；
- 人工审阅方式与需要用户决定的事项；
- 减法审计要清理的清单。

## Eval Prompt

创建 2–5 个真实用户 Prompt：

```json
{
  "id": "case-name",
  "prompt": "真实用户请求",
  "route_expected": "patch | lean | system",
  "expected_behavior_change": "这个 Skill 应让什么行为变好",
  "files": [],
  "must_do": [],
  "must_not_do": []
}
```

至少覆盖以下类别。**分级执行**：必跑 3 类（带 ★），其余按需（任务相关才跑，不要为凑数全做）：

- ★ 触发、边界与 Patch / Lean / System 路线选择；
- 先读取已有材料再提问；
- ★ 先给全景、当前 Stage 任务完整；
- 判断框架与自由度是否匹配；
- 模型和脚本分工；
- Contract 是否有真实消费者；
- 人工介入是否对应具体决定；
- 升级是否删除失效内容；
- 运行后是否自检，但只积累有证据且能改变未来行为的 Gotcha；
- ★ 最终语义质量。

只有目标 Skill 确实需要脚本、Contract 或人工关隘时，才把“使用它们”写进断言。

用例集至少同时包含：一个不应启动完整规划的 Patch、一个 Lean 新建任务、一个 System 复杂任务。不要让所有 Eval 都预设“流程越完整越好”。

## Baseline 对比

新 Skill 比较 without skill 与 with skill；重构比较 old 与 new。观察：

- 是否减少跳步和重复提问；
- 当前 Stage 是否更容易理解；
- 是否减少无意义字段、文件、命令和回执；
- 模型是否把注意力放在语义判断；
- 人工决定是否更少但更有价值；
- 真实输出是否更完整；
- Active 文件是否减少或更清楚。

**Baseline 对照的硬性要求**：必须做或显式记录跳过理由。
- 目标 Skill 存在旧版本或相邻实现 → 必须比较 with/without（或 old/new），汇报差异；
- 不存在旧版本 → 显式记录"无 baseline，跳过对照"；
- 不允许静默跳过。"可行时"不是一个条件——只有"有没有旧版本"才是。

## Forward Testing

使用干净上下文。测试模型只收到普通用户真实会提供的：

- Skill 路径；
- 用户任务；
- 输入文件；
- 输出位置。

不要泄露预期答案、诊断结论或隐藏成功标准。复杂 Skill 优先测试一轮完整真实任务，而不只让模型评论 Skill 文件。

## Human Review

主观任务由人评估真实产物。Review 围绕一个清楚决定组织：

- 结构是否批准；
- 方向是否选择；
- 内容是否可交付；
- 新版本是否优于 baseline。

展示完整核心内容，隐藏不影响决定的工程信息。

## 迭代

1. 判断失败属于 Trigger、全景、Stage、判断框架、Script、Contract、Human Checkpoint、Interface、Eval 还是最终表达。
2. 修复最低权威层。
3. 同步 Producer、Consumer 和真实行为测试。
4. 避免过拟合一个 Prompt。
5. 重跑聚焦测试和必要的上下游测试。
6. 使用 `continuous-iteration.md` 执行减法审计。
7. 使用 `failure-modes.md` 扫描六个 failure mode。

## 完成标准

- 基础结构有效；
- 每个 Reference 都有明确读取时机；
- Patch、Lean 和 System 的选路与用户设计确认行为符合预期；
- 每个 Script 都减少机械负担；
- 每个 Contract 都有真实机器消费者；
- Stage 同时具备语义完成和机器检查边界；
- 代表性 Eval 已运行，或明确说明为何暂缓；
- 减法审计已完成；
- 残余语义风险没有被绿色工程测试掩盖。
