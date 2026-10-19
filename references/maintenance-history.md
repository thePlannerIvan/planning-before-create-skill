# 维护记录：planning-before-create-skill

## 2026-10-19：轻量准则与按需调用

- 入口改为新建、升级两种用法与共同准则；移除 Patch / Lean / System 和固定里程碑，3+1 作为设计检查维度。
- 清理旧 Stage 模板的活跃指引和固定问答工具名；相邻架构 Skill 的交接改为设计、实现与验收准则。
- 模块设计与迭代说明按需读取。失败模式并入迭代说明，删除重复的本 Skill 架构表、空候选池及专用审阅页模板；历史仅在本文件保留。
- 脚手架只建入口，拒绝覆盖，取消空脚本、空候选池与强制架构文件。
- 检查器使用 YAML 解析器，只做静态结构检查；移除导入执行、跨库同名猜测、词汇与表格格式评分。新增未填骨架检查，验收路由不再限定为本 Skill 的路线。
- 工具回归覆盖真实缺陷；行为用例提供样本与可观察结果。发布前的执行结果记录在本次交付中。

---

## 2026-10-16：确定性门禁修复与减法审计补漏

### 1. 升级原因
一次真实项目运行暴露了三类问题，全部指向「判据写了但不可执行」：

- **唯一的静态质检工具在它要服务的环境里必崩**：`lint_skill.py` 用 `py_compile.compile()`
  做语法检查，它默认把 `.pyc` 写进 `~/Library/Caches/com.apple.python/`；沙箱/受限环境拒写该目录，
  于是工具以 `PermissionError` 退出 1。**它从未跑出过任何真实发现。**
- **工具名写错，且散落三处**：`SKILL.md`、`references/architecture.md`、
  `references/maintenance-history.md` 都写作 `ask_question`，系统实际工具名是 `ask_user_question`。
- **减法审计漏了 `evals/`**：`evals/evals.json` 的 `must_do`/`must_not_do` 仍在用上一轮
  退役记录里已删除的词汇（Workflow Map / Contract / Stage 文件 / development-plan.md）。
  跑这套 eval 等于把模型推回旧架构。

### 2. 核心改动
- **`scripts/lint_skill.py` 重写三处**：
  - 语法检查改为**内存内编译**（`compile(source, path, "exec")`），不再落盘 → 沙箱可运行；
  - 新增**导入冒烟**：语法合法但一 import 就炸的那一类（如 3.9 下的 `str | None` 标注）
    只有真导入才暴露，`py_compile` 永远放行；
  - 孤儿扫描从「只扫 `references/*.md`」扩到 `references/` + `assets/` + `scripts/` 三处；
    新增 `evals/` 结构与指针校验（有 evals 却没指针 = 闭环缺失）。
- **工具名一次性对齐**三处 → `ask_user_question`。
- **`evals/evals.json` 全部改写**为现行词汇，并把「不得复活已退役概念」写进 `must_not_do`；
  新增 `evals/runbook.md` 定义跑法与判据归属（判据只在 `evals.json`，跑法在 runbook）。
- **`SKILL.md` description 收紧边界**：明确本 Skill 是**执行侧**规划器，
  架构选型走 `creative-skill-architect`，消除两个 Skill 指针互相覆盖的歧义。
- **里程碑 4 的表述与代码对齐**：原文称 lint 检查「未闭环指令」，实际没这个检查；
  现按工具真正校验的六项改写。

### 3. 减法审计（本轮实际删除/回收）
- `assets/review-page-template.html`：**不是删除，是补指针**。它此前只出现在 `README.md`
  的目录树里，`SKILL.md` 从不提它，于是成为孤儿。判定为「有效资产缺导航」而非「失效沉积」，
  已在 `SKILL.md` 里程碑 1 与 `architecture.md` 模块表登记主人，并在 lint 中归类为孤儿检查对象。
- 工具名与旧词汇的重复表述：全部收敛到单一出处的写法。
- 本次升级**有增有删**：新增导入冒烟与 evals 校验、删除三处错误工具名与一整套废词汇表述。

---

## 2026-10-12：SOP 范式向 OKR + 确定性工具箱范式重大重构

### 1. 升级原因
- 旧版本将 Skill 视为流水线工人的 SOP，通过 6 道繁琐门禁与微观工步强行规训模型，导致上下文臃肿、打断用户思考心流、且缺乏真正的确定性工具支持。
- 新理念确立：模型需要的是清晰的 **OKR（意图 O + 具象判据 KR）**、**高内聚低耦合的确定性工具箱 (Tools)** 与 **启发式战术手册 (Playbook)**。大量死逻辑下沉为脚本，活逻辑与执行弹性充分放权给模型。

### 2. 核心改动
- **架构升级**：确立 3+1 核心骨架（O + KR + Tools + Playbook）。
- **流程精炼**：从 6 道审批门禁收敛为 4 个流畅的里程碑（Grill 对齐 -> 架构与工具设计 -> 脚手架生成 -> 自动化质检与核验）。
- **确定性工具就位**：
  - 新增 `scripts/scaffold_skill.py`（自动化脚手架生成器）；
  - 新增 `scripts/lint_skill.py`（自动化静态质检工具）。
- **Grill 原生复用**：废弃手写协议，直接复用系统 `/grill-me` 与 `ask_user_question`。

### 3. 减法审计（删除清单）
彻底删除 7 个 SOP 流水线时期的历史沉淀文件：
1. `references/philosophy.md`
2. `references/grill-protocol.md`
3. `references/stage-design.md`
4. `references/workflow-map-template.md`
5. `references/control-and-contracts.md`
6. `references/human-checkpoints.md`
7. `references/validation-and-iteration.md`
