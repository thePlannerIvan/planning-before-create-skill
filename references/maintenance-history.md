# 升级历史记录：planning-before-create-skill

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
- **Grill 原生复用**：废弃手写协议，直接复用系统 `/grill-me` 与 `ask_question`。

### 3. 减法审计（删除清单）
彻底删除 7 个 SOP 流水线时期的历史沉淀文件：
1. `references/philosophy.md`
2. `references/grill-protocol.md`
3. `references/stage-design.md`
4. `references/workflow-map-template.md`
5. `references/control-and-contracts.md`
6. `references/human-checkpoints.md`
7. `references/validation-and-iteration.md`
