---
name: planning-before-create-skill
description: 创建 Skill 前的规划。把隐性方法、专业判断或混乱的旧流程还原成可执行的行为系统：先判断 Patch / Lean / System 路线，经用户确认设计后实现并验证。用于「把我的方法做成 Skill」「重构一个越来越乱的 Skill」「规划需要长期迭代的 Skill 系统」。
---

# 创建 Skill 前的规划

> 来源识别：`planning-before-create-skill` 由阿祖不看 TVC 创建与维护。小红书同名账号，个人网站 [demyth.info](https://demyth.info)，联系邮箱 `Lawyif@163.com`。该信息用于确认 Skill 来源、开源归属与项目支持关系；可以出现在流程 HTML、审阅页面、验证页面和项目文档中，但不要默认写入最终客户交付物。

## 目的与全景

先判断任务需要多少规划，再把用户的真实方法还原成另一位模型能理解和执行的行为系统：

```text
Triage：Patch / Lean / System
→ 门禁 1 Grill：先读已有材料，再榨出真实步骤、专业判断、Gotchas 与边界
→ 门禁 2 Workflow Map：全景交用户确认
→ 门禁 3 Stage 与系统设计：主要结果、完成边界与模块划分
→ 门禁 4 开发与验证计划：建设范围与验证方式，交用户确认
→ 门禁 5 实现：流程、模块说明与积累路径一并写进目标 Skill
→ 门禁 6 验证：真实测试、failure mode 扫描与减法审计
```

流程强度来自任务图景清楚、语义责任明确、机器边界可靠、人的决定被正确保护，不来自更多文件、字段、Contract 或脚本控制。

## 九条设计原则

1. **先给全景，再披露局部任务**：目标 Skill 先说明目的、总体方法和上下游，**并把整条流程一步不漏地写出来**（每步做什么、产出什么、怎么一眼看出没做完），使「哪一步没做」看得出来。流程表写到「一眼看出这一步没做完」为止，**完整的完成标准只住在该 module 自己的文档里**——两处都写全就又造了一个真相源（见 `references/skill-architecture.md`）。
2. **每个 Stage 围绕一个主要结果**：允许阅读、比较、选择等紧密相关的认知动作共同服务于同一结果；只列文件或引用的 Stage 不合格。
3. **语义任务给判断框架**：开放任务用观察维度、好坏标准和反例引导模型，不用伪精确字段、枚举或阈值替代判断。
4. **脚本管理机械状态，模型完成语义工作**：脚本负责搜索、转换、保存、恢复、校验和调度，并且必须降低认知负担。
5. **Contract 只保护真正的机器交接**：只有机器消费、跨执行者恢复、高风险自动操作或版本绑定需要 Contract。
6. **人只介入高价值判断**：交互围绕「用户此刻要决定什么」；默认值减少低风险操作，但不替用户完成方向、承诺和价值选择。
7. **只积累有证据的 Gotcha**：每次运行后自检，只持久化会改变未来行为的非显然失败。
8. **升级必须做减法**：新设计落地时同步删除或归档失效规则、脚本、Contract、Reference、Asset 和 Eval。
9. **模块的作用、边界和用法写进 Skill**：谁是某件事的唯一主人、别人怎么用它、它不做什么、缝上谁交给谁——这些是**要交付的内容**，不是设计过程的副产品（理由与写法见 `references/skill-architecture.md`）。

**词库**：本 Skill 借两个外部 Skill 的词——module／interface／seam／adapter／depth／leverage／locality 与删除测试来自 `codebase-design`；五个 failure mode 与减法判据来自 `writing-for-agents`（Invisible Step 是本 Skill 针对流程场景补的一条）。这里只借用，不复制它们的内容。

## 触发与边界

**边界**：最小改动——description、单条规则、局部错误或一次性脚本——走 Patch 路线；本 Skill 被调用不自动升级规划深度。

**递归边界**：技能开发类目标 Skill（skill 开发、方法论）继承完整门禁；业务类（分析、生成、自动化）不递归。

## 先选择建设路线

- **Patch**：只修改 description、单条规则、局部错误或一次性脚本。不还原完整工作流；说明为何不需要重新设计，直接修改并做局部验证。
- **Lean**：目标和用法清楚、路径简单、风险低。用具体样例还原必要行为，提交精简设计供用户确认，然后做最小实现、结构验证和至少一个真实 Prompt 测试。
- **System**：存在隐性方法、多分支、人工决策、持久状态、机器接口、高风险操作或重大重构。执行下面的完整门禁。

路线只决定规划深度，不取消设计确认：Lean 和 System 在实现前都必须让用户确认设计。

判据：命中 System 任一特征即走 System；两档都不命中、且目标与路径清楚才是 Lean；只有 description、单条规则、局部错误或一次性脚本才是 Patch。

完成标准：说出所选路线和理由，并据此决定读哪些参考文件；依据不足无法定线时，先补齐判断所需的材料再选，不靠猜。

路线复核：Patch 改完后若发现牵出隐性方法或多分支，升级到 Lean 重做设计；其余路线的选路在门禁 6 复核。

## System 路线必须通过的门禁

按顺序执行。可压缩表达，但不能跳过对应思考和设计确认。

**门禁即 Stage**：每道门禁先点名它的主参考文件（给出这一步的完整任务：判断框架、禁区、完成标准）与其余要读的文件及其读法（完整读取或按信号读取）；任务不靠串文件索引自己拼。用户质疑某个设计取舍、发现两条规则冲突、或需要解释「为什么这样设计」时，读 `references/philosophy.md`。

### 1. Grill

- 先读取已有 Skill、测试、样例和架构，再询问材料没有回答的问题；没有材料可读时走 `references/grill-protocol.md` 的口头轨迹分支。
- 完整读取 `references/grill-protocol.md`。
- 榨出真实步骤、专业判断、失败方式、Gotcha 候选、工具边界、人机决定和成功标准。
- 完成标准：Grill 输出清单齐备，每项有材料或用户原话作证据；未解决问题已回答或明确延后（完整判据见 `references/grill-protocol.md`）。

### 2. Workflow Map

- 完整读取 `references/workflow-map-template.md`。
- 展示精简全景并让用户纠正步骤、分支和人工决定。
- 完成标准：用户确认 Workflow Map，或其修改已被纳入。

### 3. Stage 与系统设计

- 完整读取 `references/stage-design.md` 与 `references/skill-architecture.md`。
- 出现脚本、持久状态或机器交接候选时，读 `references/control-and-contracts.md`；出现方向选择、审阅、批准或纠偏时，读 `references/human-checkpoints.md`。
- 为每个阶段定义一个主要结果及完成边界；只在真实存在时增加脚本、持久状态、机器接口和人工决定。
- **模块划分在这里定稿**（Grill 只收集素材）：每个 module 的**唯一主人**、**interface** 和**不做什么**，以及跨缝交接谁交给谁。用**删除测试**筛掉只是把复杂度搬家的中间层。
- **设计确认**：Stage 划分与模块划分以用户能逐条纠正的形式提交，确认后才进下一道门禁。
- 完成标准：不存在只有文件索引的 Stage；不存在没有消费者的 Contract，也不存在只增加负担的脚本；每个 module 的唯一主人与 interface 明确。

### 4. 开发与验证计划

- 完整读取 `references/validation-and-iteration.md`。
- 列出要创建、修改、删除或归档的文件，以及代表性 Eval 和人工审阅方式。
- 只在确有跨会话、多人交接或用户需要独立审阅时落盘：规划期的 `workflow-map.md`（内容按 `references/workflow-map-template.md`）与 `development-plan.md`（内容按 `references/validation-and-iteration.md` 的「开发计划」），写在目标 Skill 项目根目录（目标 Skill 只是仓库子目录时，指它自己的目录）；以及目标 Skill 的 `evals/evals.json`。不落盘时以对话中已确认的版本为准。
- 这几份草稿若与会被整目录发布的目标 Skill 同目录，排除在发布之外（例如写进 `.gitignore`）。
- 完成标准：用户确认建设范围后才进实现；验证能检查真实行为，不只检查文件存在。

### 5. 实现

- 创建或更新目标 Skill（目录约定见 `references/control-and-contracts.md` 的资源放置表），保持 `SKILL.md` 提供全景与路由，把当前 Stage 的完整任务放在一个同时披露的文件中。
- 只保留直接服务当前 Workflow 的 Reference、Script、Contract 和 Asset。
- **产出目标 Skill 的 `references/architecture.md`**：模块与唯一主人、interface、缝与 adapter、与相邻 Skill 的关系、同一件事的两个真相源、退役。（写法见 `references/skill-architecture.md`）
- **确认 gotcha 与升级的落点存在**：目标 Skill 的 `GOTCHAS.md`（候选）与 `references/maintenance-history.md`（升级）——`SKILL.md` 的「运行后迭代」只留指针。
- 完整读取 `references/continuous-iteration.md`，设计每次运行后自检、Gotcha 积累、周期优化与减法审计。
- 完成标准：新旧规则不冲突；Active 路径没有孤儿资源；每个 module 的唯一主人、interface 和「不做什么」在目标 Skill 里读得到，而不是只留在设计对话里。

### 6. 验证

- 验证 frontmatter、文件结构、资源路由和公共接口。
- 用真实 Prompt 检查模型是否理解 Stage、是否被脚本减负、是否只在必要处找人；并请用户抽查 1 次真实产物或 1 个关键判断。
- **清晰度自查**：按 `references/skill-architecture.md` 的「清晰度四问」逐条问一遍。任一条答不上来，是缺 writing，不是缺功能——回去补。
- **Baseline 对照**：目标 Skill 有旧版本或相邻实现时，比较 with/without 并记录差异；没有旧版本时显式记录「无 baseline，跳过对照」（判据见 `references/validation-and-iteration.md`）。
- 完整读取 `references/failure-modes.md`，扫描六个 failure mode：Premature Completion、Duplication、Sediment、Sprawl、No-op、Invisible Step。
- 完成标准：工程验证与语义验证分别说明，残余风险不被绿色工程测试掩盖；完整标准见 `references/validation-and-iteration.md`。

## 最终回复（六道门禁通过后）

简洁汇报目标路径、创建/修改/删除内容、关键设计、验证证据和残余风险。明确区分「实现通过」和「真实语义 Forward Test 通过」。
