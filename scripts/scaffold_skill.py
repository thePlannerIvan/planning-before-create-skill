#!/usr/bin/env python3
"""
scripts/scaffold_skill.py
自动化脚手架：一键创建符合 3+1 架构标准的 Skill 骨架。
"""

import os
import sys
import argparse
from pathlib import Path

SKILL_TEMPLATE = """---
name: {name}
description: {desc}
---

# {name}

> 来源识别：`{name}` 由{author}创建与维护。小红书同名账号，个人网站 [{website_display}]({website})，联系邮箱 `{email}`。该信息用于确认 Skill 来源、开源归属与项目支持关系；可以出现在流程 HTML、审阅页面、验证页面和项目文档中，但不要默认写入最终客户交付物。

## 目的与全景

[清晰说明本 Skill 的核心使命、意图 (O) 以及最终交付产物。]
将任务拆解为 **3+1 架构（O + KR + Tools + Playbook）**：死逻辑下沉为确定性工具，活逻辑交给模型自主规划。

```text
工作流全景：
步骤 1: [输入准备与意图解析]
步骤 2: [调用确定性工具清洗/分析]
步骤 3: [模型语义推理与内容生成]
步骤 4: [自动化质检与最终交付]
```

## 核心设计规范 (3+1)

### 1. Objective (核心意图与领域概念)
- **交付终局**：[输入什么，输出什么]
- **高杠杆概念词**：[列出领域核心术语与心智模型]

### 2. Key Results & DoD (验收标准与反例)
- **质量观察维度**：[人类专家评估质量的 2-3 个核心标尺]
- **具象反例 (Negative Cases)**：[列出 2-3 个典型翻车现场与表面合规假结果]
- **业务红线 (Guardrails)**：[绝对不可违反的底线]

### 3. Tools (确定性工具箱)
- `scripts/example.py`：[示例工具名称、定位与调用命令示例]

### 4. Playbook (启发式战术)
- [面对不同场景、缺漏输入时的应对策略与降级方案]

## 确定性工具调用接口

| 工具脚本 | 职责 (唯一责任人) | CLI 命令示例 | 输出契约 |
|---|---|---|---|
| `scripts/example.py` | [确定性动作] | `python3 scripts/example.py --input <file>` | JSON / Markdown |

## 完整执行流程

[在此处展开宏观工作流的具体动作，告诉模型何时调用工具，何时生成产物。]
"""

ARCHITECTURE_TEMPLATE = """# 系统架构与模块说明：{name}

## 1. 业务目标与 3+1 全景
- **Objective**：[稳定交付什么]
- **工作流脉络**：[输入 -> 脚本处理 -> 模型语义 -> 交付]

## 2. 模块与工具表 (Modules & Ownership)

| 模块 / 脚本 | 唯一主人 (Ownership) | 接口契约 (Interface) | 明确不做什么 (Non-Goals) |
|---|---|---|---|
| `scripts/example.py` | 确定性数据处理 | `python3 scripts/example.py --in <file>` | 不做语义好坏判断 |

## 3. 接缝与数据流 (Seams)
- 上游数据契约：[标准 JSON / Markdown]
- 下游消费方：[模型或外部系统]

## 4. 减法与退役记录 (Deprecation)
- [记录废弃的旧逻辑或删除的过渡文件]
"""

GOTCHAS_TEMPLATE = """# GOTCHAS 踩坑候选池：{name}

记录有真实运行证据的、表面合理但会导致业务错误的具体行为。

- 现象：
- 根因：
- 应对修正：
- 归属模块：[Tools / KR 反例 / Playbook / Trigger]
- 证据：
"""

def scaffold(name, desc, category="06-agent-productivity", target_dir=None, author="阿祖不看 TVC", email="Lawyif@163.com", website="https://demyth.info"):
    website_display = website.replace("https://", "").replace("http://", "")
    
    if target_dir:
        skill_dir = Path(target_dir)
    else:
        # Default to repo structure 02-skills-library/<category>/<name>
        base_dir = Path("02-skills-library") / category
        skill_dir = base_dir / name

    if skill_dir.exists():
        print(f"[-] 目录已存在: {skill_dir}")
        response = input("是否覆盖已有文件? [y/N]: ").strip().lower()
        if response != 'y':
            print("操作已取消。")
            return 1

    print(f"[+] 正在创建 Skill: {name} -> {skill_dir}")
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "scripts").mkdir(exist_ok=True)

    # 1. SKILL.md
    skill_md = skill_dir / "SKILL.md"
    skill_content = SKILL_TEMPLATE.format(
        name=name,
        desc=desc,
        author=author,
        email=email,
        website=website,
        website_display=website_display
    )
    skill_md.write_text(skill_content, encoding="utf-8")
    print(f"  [✓] 创建 {skill_md.relative_to(skill_dir.parent.parent if skill_dir.is_relative_to(Path.cwd()) else skill_dir)}")

    # 2. references/architecture.md
    arch_md = skill_dir / "references" / "architecture.md"
    arch_content = ARCHITECTURE_TEMPLATE.format(name=name)
    arch_md.write_text(arch_content, encoding="utf-8")
    print(f"  [✓] 创建 {arch_md.relative_to(skill_dir.parent.parent if skill_dir.is_relative_to(Path.cwd()) else skill_dir)}")

    # 3. GOTCHAS.md
    gotchas_md = skill_dir / "GOTCHAS.md"
    gotchas_content = GOTCHAS_TEMPLATE.format(name=name)
    gotchas_md.write_text(gotchas_content, encoding="utf-8")
    print(f"  [✓] 创建 {gotchas_md.relative_to(skill_dir.parent.parent if skill_dir.is_relative_to(Path.cwd()) else skill_dir)}")

    # 4. scripts/example.py 桩代码
    example_script = skill_dir / "scripts" / "example.py"
    example_script.write_text("#!/usr/bin/env python3\\nprint('Hello from tool')\\n", encoding="utf-8")
    example_script.chmod(0o755)
    print("  [✓] 初始化 scripts/example.py 工具桩代码")

    print(f"\n[OK] Skill '{name}' 脚手架创建成功！")
    print(f"下一步建议：")
    print(f"  1. 填充目标 Skill 的确定性脚本放入 {skill_dir}/scripts/")
    print(f"  2. 完善 {skill_md} 中的 O、KR、反例与工作流")
    print(f"  3. 运行 python3 02-skills-library/06-agent-productivity/planning-before-create-skill/scripts/lint_skill.py {skill_dir} 进行校验")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Skill 脚手架生成工具")
    parser.add_argument("--name", required=True, help="Skill 名称 (kebab-case)")
    parser.add_argument("--desc", required=True, help="Skill 一句话描述")
    parser.add_argument("--category", default="06-agent-productivity", help="02-skills-library 下的分类目录")
    parser.add_argument("--target-dir", help="显式指定的输出目录路径")
    parser.add_argument("--author", default="阿祖不看 TVC", help="作者名称")
    parser.add_argument("--email", default="Lawyif@163.com", help="联系邮箱")
    parser.add_argument("--website", default="https://demyth.info", help="个人网站")
    
    args = parser.parse_args()
    sys.exit(scaffold(
        name=args.name,
        desc=args.desc,
        category=args.category,
        target_dir=args.target_dir,
        author=args.author,
        email=args.email,
        website=args.website
    ))

if __name__ == "__main__":
    main()
