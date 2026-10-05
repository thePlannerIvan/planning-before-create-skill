# Planning Before Create Skill

先判断任务需要 Patch、Lean 还是 System 级规划，再把隐性工作方法变成经过用户确认、能够验证和持续优化的 Skill。

作者：阿祖不看 TVC  ·  [demyth.info](https://demyth.info)  ·  `Lawyif@163.com`

## 解决什么问题

许多 Skill 不是写得不够长，而是没有把真实工作流、专业判断、工具边界、人机决定和成功标准说清楚。本 Skill 先还原工作流，再确认 workflow map、Stage、模型与脚本分工和验证计划，最后才实现目标 Skill。

它不把“强流程”理解为更多文件、Contract 和脚本控制：语义任务给模型完整图景与判断框架，脚本只承担机械状态，Contract 只保护真正的机器交接。

## 核心流程

1. Triage：局部修改走 Patch，简单新建走 Lean，隐性方法、长流程或重大重构走 System。
2. Grill：先读已有材料，再提取步骤、专业判断、失败方式、Gotchas 和边界。
3. 设计确认：Lean 确认精简设计；System 确认 Workflow Map 和建设范围。
4. 实现与验证：只创建必要资源，分别验证工程和真实语义行为。
5. 运行后迭代：每次自检，只积累有证据的 Gotcha，周期优化时合并重复项并删除失效内容。

## 适合与不适合

适合创建新 Skill、重构跳步骤的旧 Skill、设计需要人工确认的复杂流程，以及需要长期迭代但不想无限膨胀的 Skill。局部修改会自动走 Patch，不启动完整流程。

不适合把一个简单提示词快速包装成 Skill，或在工作流尚未明确时直接生成最终实现。

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

期望行为：选择 System 路线，先 grill 并产出 workflow map 供用户确认，而不是直接开始写目标 `SKILL.md`。

## 目录结构

```text
planning-before-create-skill/
├── SKILL.md
├── agents/openai.yaml
├── assets/review-page-template.html
├── evals/evals.json
└── references/         # 按 Stage 或触发信号读取的方法文件
```

## 品牌与署名边界

本项目使用 AGPL-3.0-only。许可证覆盖代码与文档，不授权冒充官方项目、暗示作者背书或未经许可使用项目品牌。修改版应改名或明确标为 fork；商业服务、私有部署和定制合作请先阅读 [COMMERCIAL.md](COMMERCIAL.md)。详见 [NOTICE](NOTICE) 与 [TRADEMARK.md](TRADEMARK.md)。

过程审阅页可以显示作者署名；本 Skill 不会默认把项目品牌写入最终客户交付物。

## 维护

每次运行后先做内部自检；只把有原始证据、会改变未来行为的 Gotcha 写入经用户确认的唯一长期位置。积累后按根因集中优化，同时合并重复项、删除失效规则和重跑代表性 Prompt。

## License

Copyright (C) 2026 阿祖不看 TVC。Released under the GNU Affero General Public License v3.0 only. See [LICENSE](LICENSE).
