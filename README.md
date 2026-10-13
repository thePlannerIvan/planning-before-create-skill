# Planning Before Create Skill

创建与重构 Skill 的系统化规划。围绕 **3+1 架构（目标 O、交付判据 KR、确定性工具箱 Tools、启发式战术 Playbook）** 为模型赋能：把大量固定规则的机械动作下沉为确定性脚本工具，把语义弹性留给模型自主规划。

作者：阿祖不看 TVC  ·  [demyth.info](https://demyth.info)  ·  `Lawyif@163.com`

## 解决什么问题

许多 Skill 不是写得不够长，而是把模型当成死板的流水线工人（SOP），缺乏清晰的目标判据、核心概念词锚点与高内聚的确定性工具支撑。
本 Skill 先将复杂任务拆解为 **3+1 架构**：用观察维度和反例引导模型判断，用高内聚低耦合的 CLI 工具接管机械死逻辑，释放模型的语义推理能力。

## 核心里程碑

1. **Triage 选路线**：局部修补走 Patch，简单新建走 Lean，隐性专业经验、工具链开发或系统重构走 System。
2. **里程碑 1 · /grill-me 探针与 OKR 对齐**：深挖核心意图 (O)、领域高杠杆概念词、验收标准与反例 (KR) 及确定性工具候选 (Tools)，一次性与用户对齐。
3. **里程碑 2 · 能力架构与工具设计**：划定 3+1 结构，定义确定性工具的 CLI 接口契约（通过删除测试筛除多余中间层）与启发式战术 (Playbook)。
4. **里程碑 3 · 工具化生成与语义注入**：调用自带 `scripts/scaffold_skill.py` 一键生成标准骨架，编写确定性脚本并注入领域知识与架构说明。
5. **里程碑 4 · 确定性质检与交付核验**：调用自带 `scripts/lint_skill.py` 进行自动化规范检查，通过真实 Prompt 验收与减法审计（Deletion Audit）后交付。

## 适合与不适合

适合把散在脑海中的专业经验做成带工具链的 Skill、重构越来越臃肿混乱的旧 Skill，以及需要长期迭代但拒绝无限膨胀的复杂系统。局部修改自动走 Patch，不启动完整流程。

## 安装

```bash
npx skills add https://github.com/thePlannerIvan/planning-before-create-skill --skill planning-before-create-skill
```

也可以克隆到 Claude Skill 目录：

```bash
git clone https://github.com/thePlannerIvan/planning-before-create-skill.git ~/.claude/skills/planning-before-create-skill
```

## 典型 Prompt

```text
我想创建一个 Skill，用来分析小红书品牌投放表格。我有自己的分析方法，但现在都散在脑子里。帮我把它变成一个 Skill。
```

期望行为：选择 System 路线，启动 `/grill-me` 提炼 OKR 蓝图、核心概念词与确定性脚本清单供用户确认，确认后通过脚手架生成、实现工具并通过静态质检。

## 目录结构

```text
planning-before-create-skill/
├── SKILL.md                            # 核心主入口（全景、八大设计原则、四里程碑流程）
├── GOTCHAS.md                          # 踩坑候选池
├── agents/openai.yaml
├── assets/review-page-template.html
├── evals/evals.json
├── references/                         # 高杠杆领域架构规范与审计字典
│   ├── architecture.md                 # 本 Skill 的模块所有权与接口说明
│   ├── skill-architecture.md           # 深模块、接缝与删除测试规范
│   ├── failure-modes.md                # 六大失败模式（减法审计标准字典）
│   ├── continuous-iteration.md         # 运行后自检与 Gotcha 双轨制演进
│   └── maintenance-history.md          # 重大版本升级与退役记录
└── scripts/                            # 确定性工具箱
    ├── scaffold_skill.py               # 自动化脚手架生成器
    └── lint_skill.py                   # 确定性静态合规与断链校验器
```

## 品牌与署名边界

本项目使用 AGPL-3.0-only。许可证覆盖代码与文档，不授权冒充官方项目、暗示作者背书或未经许可使用项目品牌。修改版应改名或明确标为 fork；商业服务、私有部署和定制合作请先阅读 [COMMERCIAL.md](COMMERCIAL.md)。详见 [NOTICE](NOTICE) 与 [TRADEMARK.md](TRADEMARK.md)。

过程审阅页可以显示作者署名；本 Skill 不会默认把项目品牌写入最终客户交付物。

## 维护

每次运行后做内部静默自检；只把有原始证据、会改变未来行为的 Gotcha 记入候选池 `GOTCHAS.md`。周期升级时，确定性错误下沉为 `scripts/` 工具，语义误判补充为具象反例，同时执行减法审计清理失效规则。

## License

Copyright (C) 2026 阿祖不看 TVC。Released under the GNU Affero General Public License v3.0 only. See [LICENSE](LICENSE).
