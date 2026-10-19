# Planning Before Create Skill

创建与升级 Skill 的轻量准则。入口说明共同原则与两种用法，模块设计、持续迭代和验收资料按需读取。

作者：阿祖不看 TVC · [demyth.info](https://demyth.info) · `Lawyif@163.com`

## 使用

- 新建：“把我的客户访谈分析方法做成一个 Skill。”
- 升级：“这个 Skill 的规则开始冲突，请找出原因，给出精简方案。”
- 局部修改：“只改这个 Skill 的触发描述，保持其他行为。”

具体准则和资源入口见 [SKILL.md](SKILL.md)。3+1 是检查设计是否完整的四个维度，文件和流程按需要组织。

## 安装

```bash
npx skills add https://github.com/thePlannerIvan/planning-before-create-skill --skill planning-before-create-skill
```

## 工具与验证

需要生成入口时使用 `scripts/scaffold_skill.py`，默认只写 `SKILL.md`，已有目录会被拒绝。它生成待填写的草稿，完成后再验收。

```bash
python3 scripts/scaffold_skill.py --name my-skill --desc "用途与触发场景" --target-dir /path/to/my-skill
```

静态检查器依赖 Python 3.9+ 与 PyYAML，可在已有 Python 环境或虚拟环境中安装依赖：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/lint_skill.py /path/to/my-skill
python3 -m unittest discover -s tests -v
```

检查器只读取文件，检查 YAML 元数据、入口与参考文档中的本地 Markdown 文件链接、未完成骨架标记、活动 Python 文件的语法，以及存在的 `evals/evals.json` 结构。代码中的路径缺失时提示人工核对，可能是示例或外部路径，不算已确认的有效引用。用例样本路径按 evals 目录或 Skill 根目录解析。它不导入被检查脚本，不检查外部 Skill 是否安装，不证明架构或业务结果正确。孤儿文件由升级审计结合实际调用方判断。

模型行为验收见 [evals/runbook.md](evals/runbook.md)。`tests/test_tools.py` 用临时目录验证工具行为，测试结束自动清理。

## 来源与授权

本项目使用 AGPL-3.0-only。许可证覆盖代码与文档，不授权冒充官方项目或暗示作者背书。修改版应改名或明确标为 fork；商业使用与合作说明见 [COMMERCIAL.md](COMMERCIAL.md)，来源与品牌边界见 [NOTICE](NOTICE)、[TRADEMARK.md](TRADEMARK.md)。最终客户交付物署名按项目约定处理。

Copyright (C) 2026 阿祖不看 TVC。See [LICENSE](LICENSE).
