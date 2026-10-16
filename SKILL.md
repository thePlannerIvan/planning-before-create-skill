---
name: planning-before-create-skill
description: 把专业经验做成带工具链的 Skill、或重构越来越乱的旧 Skill 的**执行侧**规划器。按 3+1 架构（O 目标 + KR 判据 + Tools 确定性工具 + Playbook 战术）拆解，用脚手架生成骨架、把死逻辑下沉成脚本、再用 lint_skill 与 evals 收口交付。架构选型（Project Grounding / Method System / Work Pipeline 那套）走 creative-skill-architect，本 Skill 承接已定架构下的流程还原、工具建造与交付核验。触发：「帮我把这套专业经验做成 Skill」「重构这个旧 Skill」「给 Skill 补工具链和质检」「Skill 该怎么规划」。
---

# 创建 Skill 前的规划

> 来源识别：`planning-before-create-skill` 由阿祖不看 TVC 创建与维护。小红书同名账号，个人网站 [demyth.info](https://demyth.info)，联系邮箱 `Lawyif@163.com`。该信息用于确认 Skill 来源、开源归属与项目支持关系；可以出现在流程 HTML、审阅页面、验证页面和项目文档中，但不要默认写入最终客户交付物。

## 目的与全景

为模型构建高内聚、低耦合的领域能力系统，而不是机械死板的微操流水线。
将复杂任务拆解为 **3+1 架构（O + KR + Tools + Playbook）**：把大量死逻辑下沉为确定性工具，把活逻辑交给模型自主规划。

规划工作流保持全景清晰，执行四个关键里程碑：

```text
Triage 选路线：Patch / Lean / System
→ 里程碑 1 /grill-me 探针与 OKR 对齐：深挖意图、概念、判据与工具候选，与用户对齐
→ 里程碑 2 能力架构与工具设计：定 3+1 结构，明确确定性工具 CLI 接口与启发式战术
→ 里程碑 3 工具化生成与语义注入：脚手架脚本一键生成骨架，注入领域经验与工具实现
→ 里程碑 4 确定性质检与交付核验：静态校验脚本跑通，真实 Prompt 验收，减法审计后交付
```

## 八条设计原则

1. **OKR 牵引而非步骤规训**：目标 Skill 优先说明核心意图 (O) 与具象好坏判据 (KR/DoD)。用清晰、明了的语言描述清楚整个任务完成的流程，用观察维度和反例（Negative Cases）引导模型，不靠事无巨细的步骤捆绑模型的思考手脚。
2. **确定性下沉 (Deterministic Offloading)**：大量规则固定、有唯一对错的机械动作（计算、格式转换、静态检查、脚手架），建议写成确定性脚本（Python/CLI/正则）。这不需要模型每次消耗上下文重写代码，模型只需按接口调用。
3. **工具高内聚低耦合**：
   - **高内聚**：一个工具自包含一项具体能力，内部逻辑封闭，不把半成品逻辑甩给模型在外面打补丁；
   - **低耦合**：工具通过标准 CLI 参数或纯数据接口（JSON/Markdown/标准输入输出）交互，不依赖隐藏上下文。
4. **Agent 上下文自治**：非必要时刻不用设计复杂的内部状态机、Dispatcher 调度协议或繁重的阶段交接 Contract。工具保持无状态，业务状态由 Agent 自身的工作记忆自然持有。
5. **概念杠杆词是高密度认知锚点**：从领域知识中提取精准的专业术语作为核心概念（Deep Module、Seam、Interface、Leverage、Locality、Deletion Test、DoD），优先使用具体的核心概念而非事无巨细的规则描述，杜绝用字数、枚举等伪精确规则替代专业理解。
6. **人机协作保护决策心流**：人不是流程审批机。在不可替代的节点让用户介入（前期的意图与终局对齐、核心的分水岭决策与价值判断、最终产物的验收），其余推演与执行充分放权给模型与工具。
7. **模块的唯一主人、接口与不做什么写进 Skill**：谁是某件事的唯一责任人、对外暴露什么接口、明确不做什么——这些要写入目标 Skill 的 `references/architecture.md`。
8. **升级必须做减法 (Deletion Audit)**：每次重构或发布前，必须进行减法审计（扫描 `references/failure-modes.md`），清理无效的中间层、失效规则与孤儿文件；踩坑与持续迭代规范遵循 `references/continuous-iteration.md`。

**词库**：借用外部 Skill `codebase-design` 的核心杠杆词——`module`／`interface`／`seam`／`depth`／`leverage`／`locality` 与 `删除测试`；借用 `writing-for-agents` 的 `failure-modes` 与减法判据。

## 触发与边界

- **Patch**：只修改 description、单条规则、局部错误或单点脚本优化。不重构全景架构，直接修改并做局部验证。
- **Lean**：目标清晰、路径简单、无深层工具链依赖。快速对齐 OKR，做最小 3+1 实现（极简工具或无工具），通过真实 Prompt 验收。
- **System**：具备隐性专业经验、多场景分支、确定性工具链需求或复杂系统重构。执行完整的四个里程碑。

判据：存在工具链开发、隐性专业判断沉淀或系统重构即走 System；无需工具链且路径单一走 Lean；局部修补走 Patch。

---

## System 路线完整执行流程

流程对模型保持透明，按顺序推进。不在中间非关键节点频繁打断用户，但每个里程碑的具体动作清晰明确。

### 里程碑 1：/grill-me 探针与 OKR 对齐
1. **背景阅读**：先读取已有材料、旧 Skill、业务代码或样例输入输出。
2. **启动 /grill-me 交互机制**（使用 `ask_user_question` 工具逐一分支推进）：
   - **核心意图 (O)**：用户究竟要解决什么本质问题？真实交付物长什么样？
   - **高杠杆概念词**：从用户的回答中思考，该领域的核心概念是什么？优先使用具体的核心概念而非事无巨细的描述和规则。
   - **验收标准与反例 (KR)**：怎么一眼看出做砸了？有哪些经典误区与负例？
   - **确定性工具候选 (Tools)**：哪些环节是固定的死逻辑，适合沉淀为独立脚本？
3. **人机对齐**：向用户呈现提炼出的 **OKR 蓝图、概念锚点与工具边界清单**。用户确认后，直接推进至下一阶段。
   要让用户在页面上做决定（而不只是在对话里回一句），用 `assets/review-page-template.html`
   起一个决策确认页；交付前必须跑 `planners-review-core/scripts/inline_review_tokens.py`
   把设计令牌内联进去——**不内联就毫无样式，而且不会报错**。

### 里程碑 2：能力架构与工具设计
1. **输入准备**：完整读取 `references/skill-architecture.md`。
2. **拆解 3+1 架构**：
   - **O & KR 规范**：提炼目标的端到端定义与交付完成线（DoD），列出典型负例与边界禁区；
   - **Tools 接口契约**：设计确定性脚本的输入输出、参数与 CLI 格式。用**删除测试**检验：删掉这个工具，复杂度是真正消失了，还是只是把代码搬家？
   - **Playbook 启发式战术**：梳理常见场景、分支策略与异常退避路径。
3. **交接确认**：如涉及跨系统缝隙（Seam）或重要技术选型冲突，在此处简要对齐一次，否则直接进入实现。

### 里程碑 3：工具化生成与语义注入
1. **一键脚手架**：调用自带工具 `python3 scripts/scaffold_skill.py --name <skill-name> --category <cat> --desc "<desc>"`，自动创建标准目录、带合规声明的 `SKILL.md` 及基础文件，消除手工机械消耗。
2. **沉淀确定性脚本**：将死逻辑固化为 Python/CLI 脚本写入目标 Skill 的 `scripts/`，并进行独立的命令行功能测试。
3. **注入活语义与 Playbook**：编写目标 Skill 的 `SKILL.md`，明确意图、DoD、工具接口说明与场景战术。
4. **交付架构说明**：产出目标 Skill 的 `references/architecture.md`，明确每个模块的唯一主人、接口标准、接缝（Seam）与不做什么。

### 里程碑 4：确定性质检与交付核验
1. **自动化规范质检**：运行自带工具 `python3 scripts/lint_skill.py <path-to-skill>`（退出码 0/1）。它确定性校验：frontmatter 合规、失效链接、`references/`+`assets/`+`scripts/` 三处孤儿、脚本语法、**脚本导入冒烟**（语法过但一 import 就炸的那一类），以及 `evals/` 的结构与指针。要求 0 error。
2. **真实 Prompt 语义验收**：`evals/evals.json` 里那几条就是验收用例（每条带 `route_expected` 与 `must_do`/`must_not_do`），跑法见 `evals/runbook.md`。至少跑通与本次改动相关的那一条，看模型是否理解了意图、是否按场景调用了 `scripts/` 工具。
3. **减法审计 (Deletion Audit)**：读取 `references/failure-modes.md`，扫描是否有冗余中间层、伪精确字段或未使用的死规则；**并同步清理这套规则在 `evals/` 里的残留表述**——eval 里留着已废弃的词汇会把模型推回旧架构。完成清理。
4. **最终交付**：向用户汇报生成结果、工具清单、测试证据与关键决策。
