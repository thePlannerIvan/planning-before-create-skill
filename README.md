# Planning Before Create Skill

在真正编写 `SKILL.md` 之前，把隐性工作方法变成经过确认的 workflow map、开发计划、验证计划和持续迭代机制。

作者：阿祖不看 TVC  ·  [demyth.info](https://demyth.info)  ·  `Lawyif@163.com`

## 解决什么问题

许多 Skill 不是写得不够长，而是没有把真实工作流、工具边界、人机介入点、输入输出合约和成功标准说清楚。本 Skill 强制先 grill，再做 workflow map 和开发/验证计划，最后才实现和验证目标 Skill。

## 核心流程

1. Grill：提取工作步骤、分支、资料、工具、边界、人工检查点和成功标准。
2. Workflow Map：把访谈结果转成可确认的流程图谱与输入输出合约。
3. 开发与验证计划：规划 references、scripts、assets、evals 和 review 方式。
4. 实现：保持 `SKILL.md` 精简，把详细知识下沉到配套资源。
5. 验证：检查 frontmatter、文件结构、真实 prompt 行为和五类失败模式。
6. 持续迭代：设计 Memory Audit、反馈收集、升级路径和防止内容沉积的机制。

## 适合与不适合

适合创建新 Skill、重构跳步骤的旧 Skill、设计需要人工确认的复杂流程，以及需要长期迭代但不想无限膨胀的 Skill。

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

期望行为：先 grill 并产出 workflow map，而不是直接开始写目标 `SKILL.md`。

## 目录结构

```text
planning-before-create-skill/
├── SKILL.md
├── agents/openai.yaml
├── assets/review-page-template.html
├── evals/evals.json
└── references/
```

## 品牌与署名边界

本项目使用 AGPL-3.0-only。许可证覆盖代码与文档，不授权冒充官方项目、暗示作者背书或未经许可使用项目品牌。修改版应改名或明确标为 fork；商业服务、私有部署和定制合作请先阅读 [COMMERCIAL.md](COMMERCIAL.md)。详见 [NOTICE](NOTICE) 与 [TRADEMARK.md](TRADEMARK.md)。

过程审阅页可以显示作者署名；本 Skill 不会默认把项目品牌写入最终客户交付物。

## 维护

运行后优先记录具体反馈，再判断它应进入一次性项目产物、reference、脚本、Skill 本体还是 eval。每次升级都应重新执行结构检查和代表性 prompt 验证。

## License

Copyright (C) 2026 阿祖不看 TVC。Released under the GNU Affero General Public License v3.0 only. See [LICENSE](LICENSE).
