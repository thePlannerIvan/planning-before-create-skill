#!/usr/bin/env python3
"""Read-only structural checks. Never imports or executes the inspected Skill."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__",
             "archive", "_archive", "tests", "fixtures", "vendor", "lib"}
PATH_PATTERN = re.compile(r"(?<![\w/.-])(?:references|scripts|assets|helpers|evals)/[\w./-]+")
PLACEHOLDER = re.compile(r"\[TODO:[^\]\n]*\]")


def active(path, root):
    return not path.is_symlink() and not (set(path.relative_to(root).parts) & SKIP_DIRS)


def parse_frontmatter(text):
    import yaml
    match = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.S)
    if not match:
        raise ValueError("缺少完整的 YAML frontmatter")
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"YAML 无效：{exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("frontmatter 必须是字段映射")
    return data


def references(text):
    """Explicit Markdown links and conventional local paths; not a call graph."""
    for target in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)", text):
        target = target.strip().strip("<>")
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith(("/", "#")):
            continue
        yield target.split("#", 1)[0], False
    for target in PATH_PATTERN.findall(text):
        # Generic directory names and patterns are not concrete file references.
        if Path(target).suffix:
            yield target.rstrip("."), True


def check_evals(path):
    errors = []
    try:
        blob = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return [f"evals JSON 无效：{exc}"]
    cases = blob.get("evals") if isinstance(blob, dict) else blob
    if not isinstance(cases, list) or not cases:
        return ["evals 必须是非空数组或包含非空 evals 数组的对象"]
    ids = set()
    for index, case in enumerate(cases):
        label = f"evals[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label} 必须是对象")
            continue
        eid = case.get("id")
        if not isinstance(eid, (str, int)) or isinstance(eid, bool) or not str(eid).strip():
            errors.append(f"{label} 缺少有效 id")
        elif str(eid) in ids:
            errors.append(f"{label} id 重复：{eid}")
        else:
            ids.add(str(eid))
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{label} 缺少非空 prompt")
        meaningful = False
        for key in ("must_do", "must_not_do", "expectations"):
            if key in case:
                value = case[key]
                if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
                    errors.append(f"{label}.{key} 必须是非空字符串组成的数组")
                elif value:
                    meaningful = True
        for key in ("expected_behavior_change", "expected_output"):
            if key in case:
                value = case[key]
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{label}.{key} 必须是非空字符串")
                else:
                    meaningful = True
        if not meaningful:
            errors.append(f"{label} 缺少可观察的验收判据")
        if "files" in case:
            files = case["files"]
            if not isinstance(files, list) or any(not isinstance(f, str) or not f.strip() for f in files):
                errors.append(f"{label}.files 必须是路径字符串数组")
            else:
                for filename in files:
                    if not any((base / filename).exists() for base in (path.parent, path.parent.parent)):
                        errors.append(f"{label} 样本不存在：{filename}")
    return errors


def lint_skill(skill_path, warnings=None):
    root = Path(skill_path).resolve()
    warnings = [] if warnings is None else warnings
    errors = []
    if not root.is_dir():
        return [f"Skill 目录不存在：{root}"]
    entry = root / "SKILL.md"
    if not entry.is_file():
        return ["缺少 SKILL.md"]
    try:
        text = entry.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        name = fm.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append("name 必须是 1–64 字符的 kebab-case 名称")
        elif name != root.name:
            errors.append("name 与目录名不一致")
        if not isinstance(fm.get("description"), str) or not fm["description"].strip():
            errors.append("description 必须是非空字符串")
    except (ValueError, OSError) as exc:
        errors.append(f"SKILL.md：{exc}")
    docs = [entry] + sorted((root / "references").rglob("*.md"))
    for doc in docs:
        if not active(doc, root) or doc.name == "maintenance-history.md":
            continue
        try:
            content = doc.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"无法读取 {doc.relative_to(root)}：{exc}")
            continue
        if PLACEHOLDER.search(content):
            errors.append(f"{doc.relative_to(root)} 有未填写的骨架标记")
        missing = set()
        for target, conventional in references(content):
            if not target:
                continue
            # Markdown links are relative to their document; bare conventional paths are Skill-root-relative.
            resolved = (root if conventional else doc.parent) / target
            if not resolved.exists():
                if conventional:
                    warnings.append(f"{doc.relative_to(root)} 代码中的路径需核对（可能是示例或外部路径）：{target}")
                else:
                    missing.add(target)
        errors.extend(f"{doc.relative_to(root)} 本地引用不存在：{ref}" for ref in sorted(missing))
    for script in sorted(root.rglob("*.py")):
        if not active(script, root):
            continue
        try:
            compile(script.read_bytes(), str(script), "exec")
        except (SyntaxError, ValueError, OSError) as exc:
            errors.append(f"{script.relative_to(root)} 语法检查失败：{exc}")
    eval_file = root / "evals/evals.json"
    if eval_file.is_file():
        errors.extend(check_evals(eval_file))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Skill 根目录；退出码 0=结构项通过，1=发现错误，2=缺少依赖")
    args = parser.parse_args()
    warnings = []
    try:
        errors = lint_skill(args.path, warnings)
    except ModuleNotFoundError as exc:
        if exc.name != "yaml":
            raise
        print("ERROR: 缺少 PyYAML；请在所用 Python 环境中安装 requirements.txt 中的依赖。", file=sys.stderr)
        return 2
    for warning in sorted(set(warnings)):
        print(f"REVIEW: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"结构检查未通过：{len(errors)} 项错误。")
        return 1
    if warnings:
        print(f"静态检查未发现确定错误；{len(set(warnings))} 处路径需要人工核对。")
    else:
        print("所检查的静态结构项通过。")
    print("未执行脚本，也未验证架构与业务效果。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
