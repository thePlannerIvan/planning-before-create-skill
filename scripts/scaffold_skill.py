#!/usr/bin/env python3
"""Create a minimal Skill draft without overwriting an existing directory."""
import argparse
import json
import re
import sys
from pathlib import Path


def scaffold(name, desc, category="06-agent-productivity", target_dir=None,
             author="阿祖不看 TVC", email="Lawyif@163.com", website="https://demyth.info"):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError("name 必须是 1–64 字符的小写字母、数字及连接用连字符")
    if not isinstance(desc, str) or not desc.strip():
        raise ValueError("description 不能为空")
    if not target_dir and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", category):
        raise ValueError("category 必须是单个分类目录名")
    target = Path(target_dir) if target_dir else Path("02-skills-library") / category / name
    if target.name != name:
        raise ValueError("输出目录名必须与 name 一致")
    if target.exists() or target.is_symlink():
        raise ValueError(f"目录已存在，未修改任何文件：{target}")
    # JSON strings are valid YAML scalars, including descriptions containing ':' or newlines.
    description = json.dumps(desc.strip(), ensure_ascii=False)
    content = f"""---
name: {name}
description: {description}
---

# {name}

> 来源：{author} · {website} · `{email}`。最终客户交付物的署名按项目约定处理。

## 目标与判据

[TODO: 说明输入、交付结果、成功标准和一个具体反例。]

## 工作方式

[TODO: 写入完成任务所需的专业判断与场景指引；工具和参考资料按需添加。]
"""
    target.mkdir(parents=True, exist_ok=False)
    (target / "SKILL.md").write_text(content, encoding="utf-8")
    print(f"已创建草稿：{target / 'SKILL.md'}；填写 TODO 后用真实任务验收。")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument("--desc", required=True)
    parser.add_argument("--category", default="06-agent-productivity")
    parser.add_argument("--target-dir", help="输出目录；必须不存在且目录名与 name 一致")
    parser.add_argument("--author", default="阿祖不看 TVC")
    parser.add_argument("--email", default="Lawyif@163.com")
    parser.add_argument("--website", default="https://demyth.info")
    try:
        return scaffold(**vars(parser.parse_args()))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
