#!/usr/bin/env python3
"""
scripts/lint_skill.py
确定性质检工具：静态扫描 Skill 的 Frontmatter、内部引用、深模块架构与失败模式。
"""

import os
import sys
import re
import argparse
import py_compile
from pathlib import Path

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

NO_OP_PHRASES = [
    "请务必认真思考", "一定要专业严谨", "请给出高质量", "尽力做到最好",
    "仔细分析", "认真对待", "请发挥你的专业能力"
]

def parse_frontmatter(content):
    if not content.startswith("---"):
        return None, "文件未以 YAML Frontmatter (---) 开头"
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, "YAML Frontmatter 未正确闭合 (缺少第二个 ---)"
    
    raw_fm = parts[1].strip()
    data = {}
    for line in raw_fm.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            data[key.strip()] = val.strip().strip("'\"")
    return data, None

def lint_skill(skill_path_str):
    skill_dir = Path(skill_path_str).resolve()
    if not skill_dir.is_dir():
        print(f"{RED}[ERROR] 路径不是一个目录: {skill_dir}{RESET}")
        return 1

    errors = []
    warnings = []
    passes = []

    print(f"\n{BOLD}{CYAN}=== 正在静态质检 Skill: {skill_dir.name} ==={RESET}")
    print(f"路径: {skill_dir}\n")

    # 1. 检查 SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("缺少核心入口文件: SKILL.md")
        return print_summary(errors, warnings, passes)

    skill_content = skill_md.read_text(encoding="utf-8")
    fm, fm_err = parse_frontmatter(skill_content)
    if fm_err:
        errors.append(f"Frontmatter 解析错误: {fm_err}")
    else:
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            errors.append("Frontmatter 缺少 'name' 字段")
        elif name != skill_dir.name:
            warnings.append(f"Frontmatter 中的 name ('{name}') 与目录名 ('{skill_dir.name}') 不一致")
        else:
            passes.append(f"Frontmatter 'name' 合规: {name}")

        if not desc:
            errors.append("Frontmatter 缺少 'description' 字段或描述为空")
        else:
            passes.append(f"Frontmatter 'description' 存在 ({len(desc)} 字)")

    # 2. 检查 3+1 核心元素在 SKILL.md 中的存在性
    keywords_3plus1 = {
        "意图/目标 (O)": ["目的", "目标", "全景", "Objective"],
        "交付判据 (KR)": ["判据", "验收", "DoD", "反例", "Negative Cases"],
        "确定性工具 (Tools)": ["Tools", "工具", "scripts", "脚本"],
        "战术策略 (Playbook)": ["Playbook", "战术", "流程", "策略", "里程碑"]
    }
    for label, keys in keywords_3plus1.items():
        if any(k.lower() in skill_content.lower() for k in keys):
            passes.append(f"包含 3+1 架构要素: {label}")
        else:
            warnings.append(f"SKILL.md 中未显式发现 3+1 架构要素: {label}")

    # 3. 检查内部文件引用完整性 (Broken Links)
    # 查找所有 references/xxx.md 或 scripts/xxx
    ref_pattern = re.compile(r'(?:references|scripts)/[\w\-\.]+')
    found_refs = set(ref_pattern.findall(skill_content))
    
    # 也扫描 references/ 目录内文件的互相引用 (跳过维护历史记录文件，因其包含已删除文件记录)
    ref_dir = skill_dir / "references"
    if ref_dir.exists():
        for r_file in ref_dir.glob("*.md"):
            if r_file.name == "maintenance-history.md":
                continue
            r_content = r_file.read_text(encoding="utf-8")
            found_refs.update(ref_pattern.findall(r_content))

    for ref in found_refs:
        target_file = skill_dir / ref
        if not target_file.exists():
            errors.append(f"失效的文件引用 (Broken Link): 引用了 '{ref}'，但文件不存在")
        else:
            passes.append(f"有效引用: {ref}")

    # 4. 检查孤儿 Reference (Sediment 检查)
    if ref_dir.exists():
        for r_file in ref_dir.glob("*.md"):
            ref_rel = f"references/{r_file.name}"
            # architecture.md 和 maintenance-history.md 是标准约定的系统文件，不视为孤儿
            if r_file.name in ["architecture.md", "maintenance-history.md"]:
                continue
            if ref_rel not in skill_content:
                warnings.append(f"孤儿文件 (未在 SKILL.md 中引用，可能属于历史沉积 Sediment): {ref_rel}")

    # 5. 检查 references/architecture.md 是否存在
    arch_md = skill_dir / "references" / "architecture.md"
    if not arch_md.exists():
        warnings.append("缺少系统架构说明书: references/architecture.md (深模块与所有权规范推荐具备)")
    else:
        passes.append("具备系统架构说明书: references/architecture.md")

    # 6. 检查 scripts/ 脚本语法与可执行性
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for py_script in scripts_dir.glob("*.py"):
            try:
                py_compile.compile(str(py_script), doraise=True)
                passes.append(f"Python 脚本语法合法: scripts/{py_script.name}")
            except py_compile.PyCompileError as e:
                errors.append(f"Python 脚本存在语法错误: scripts/{py_script.name} -> {e}")

    # 7. No-op 废话检查
    for phrase in NO_OP_PHRASES:
        if phrase in skill_content:
            warnings.append(f"发现 No-op 弱指令 (建议替换为具体判断标准或反例): '{phrase}'")

    return print_summary(errors, warnings, passes)

def print_summary(errors, warnings, passes):
    print(f"{BOLD}--- 质检明细 ---{RESET}")
    for p in passes:
        print(f"  {GREEN}[PASS]{RESET} {p}")
    for w in warnings:
        print(f"  {YELLOW}[WARN]{RESET} {w}")
    for e in errors:
        print(f"  {RED}[FAIL]{RESET} {e}")

    print(f"\n{BOLD}--- 质检结论 ---{RESET}")
    print(f"通过项: {GREEN}{len(passes)}{RESET} | 警告项: {YELLOW}{len(warnings)}{RESET} | 错误项: {RED}{len(errors)}{RESET}")

    if errors:
        print(f"{RED}{BOLD}❌ 质检未通过！请修正上述错误项后再交付。{RESET}\n")
        return 1
    elif warnings:
        print(f"{YELLOW}{BOLD}⚠️ 质检通过，但存在优化建议。{RESET}\n")
        return 0
    else:
        print(f"{GREEN}{BOLD}✅ 完美通过！符合高内聚低耦合与 3+1 架构标准。{RESET}\n")
        return 0

def main():
    parser = argparse.ArgumentParser(description="Skill 确定性质检工具")
    parser.add_argument("path", help="Skill 根目录路径")
    args = parser.parse_args()
    sys.exit(lint_skill(args.path))

if __name__ == "__main__":
    main()
