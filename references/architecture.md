# 系统架构与模块说明：planning-before-create-skill

## 1. 业务目标与 3+1 全景
- **Objective**：创建与重构 Skill 的系统化规划能力。将复杂任务拆解为 3+1 架构（O + KR + Tools + Playbook），下沉死逻辑至确定性脚本，赋予模型充分的语义弹性与自主权。
- **工作流脉络**：Triage 选路线 -> /grill-me 探针深挖与 OKR 对齐 -> 能力架构设计与工具契约 -> 脚本脚手架生成与语义注入 -> 自动化静态质检与减法审计。

---

## 2. 模块与工具表 (Modules & Ownership)

| 模块 / 脚本 | 唯一主人 (Ownership) | 接口契约 (Interface) | 明确不做什么 (Non-Goals) |
|---|---|---|---|
| `scripts/scaffold_skill.py` | 自动化脚手架生成 | CLI: `--name`, `--category`, `--desc`, `--target-dir` | 不编写业务 Prompt 逻辑 |
| `scripts/lint_skill.py` | 静态合规与引用校验（唯一处） | CLI: `python3 lint_skill.py <path>`，退出码 0/1。校验 frontmatter、失效链接、`references/`+`assets/`+`scripts/` 三处孤儿、脚本语法、**脚本导入冒烟**、`evals/` 结构与指针 | 不替代真实 Prompt 语义测试；不做运行期阻断 |
| `evals/evals.json` | 语义验收用例的唯一出处（判据 = 每条自带的 `route_expected` 与 `must_do`/`must_not_do`） | 纯数据 JSON；`evals/runbook.md` 是它的跑法 | 不重复描述判据（判据只在用例里）；不记录运行日志 |
| `evals/runbook.md` | 语义验收的执行流程 | 指导文档：怎么起干净上下文、怎么判过/不过 | 不定义判据本身（那是 `evals.json` 的事） |
| `assets/review-page-template.html` | 人机决策确认页的唯一起点 | 需先用 `planners-review-core/scripts/inline_review_tokens.py` 内联设计令牌（占位符 `/*__DSH_TOKENS__*/`） | 不是正式审阅面；不内联就没有任何样式且不报错 |
| `references/skill-architecture.md` | 深模块与系统架构规范 | 指导文档，定义 module, interface, seam, depth, deletion test | 不包含具体业务领域知识 |
| `references/failure-modes.md` | 减法审计标准字典 | 质量扫描字典，定义六大 failure modes | 不作为运行期流水线阻断器 |
| `references/continuous-iteration.md` | 持续演进与 Gotcha 双轨制 | 指导文档，定义 GOTCHAS.md 与 maintenance-history.md | 不记录一次性运行日志 |

---

## 3. 接缝与外部系统交互 (Seams)
- **输入源**：用户的业务意图口述、旧版 Skill 文件、业务代码或历史输入输出样例。
- **Grill 交互面**：直接对接系统原生 `/grill-me` 与 `ask_user_question` 机制，不额外造轮子。
- **审阅面**：需要人在页面上做决定时，经 `assets/review-page-template.html` 输出决策确认页；
  设计令牌的唯一来源是 `planners-review-core`，**不复制令牌表**。
- **产物交付面**：符合 `02-skills-library` 规范的新 Skill 目录，准备发布至 Codex, Claude, Antigravity 运行时。

---

## 4. 减法与退役记录 (Deprecation)
本次重大重构进行了彻底的减法审计，废弃并删除了 7 个 SOP 流水线时期的历史遗留文件：
1. `philosophy.md`（旧设计哲学）：核心原则收敛合并入 `SKILL.md`，删除冗余文件。
2. `grill-protocol.md`（旧 Grill 协议）：废弃自造协议，直接调用系统原生 `/grill-me` 机制。
3. `stage-design.md`（旧 Stage 模板）：废弃流水线 Stage 模板，升级为 3+1 架构。
4. `workflow-map-template.md`（旧流程图模板）：废弃 SOP 流程图模板。
5. `control-and-contracts.md`（旧管控与契约）：废弃 Dispatcher 调度器与中间 Contract 概念。
6. `human-checkpoints.md`（旧审批卡点）：废弃繁琐审批卡点，合并入原则 6（保护决策心流）。
7. `validation-and-iteration.md`（旧验证文件）：验证流程精炼合并入里程碑 4。
