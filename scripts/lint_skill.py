#!/usr/bin/env python3
"""
scripts/lint_skill.py
确定性质检工具：静态扫描 Skill 的 Frontmatter、内部引用、深模块架构与失败模式。

## 为什么不落盘编译（2026-10-16 修）

原实现用 `py_compile.compile(path, doraise=True)` 做语法检查，它**默认把 .pyc 写进
`~/Library/Caches/com.apple.python/`**。在沙箱/受限环境（DSH 的文件策略）里那是拒写目录，
于是整个工具**在它要服务的环境里必崩**：

    PermissionError: [Errno 1] Operation not permitted:
      '.../Library/Caches/com.apple.python/.../lint_skill.cpython-39.pyc'
    exit=1

它一次都没跑出过真实发现，只是崩。这里改成**内存内编译**（`compile(source, path, "exec")`），
既不落盘也不依赖可写缓存目录。

同时补上三处它自称做了、其实没做或做得不全的检查（详见各段注释）：
孤儿的扫描面、资产的引用面、`evals/` 的结构与指针。
"""

# 标注延迟求值：`str | None` 这类 PEP 604 写法在 3.9 下会在**定义时**抛 TypeError，
# 而语法检查查不出来（那是运行期错误，不是语法错误）。加这一行，工具本身能在 3.9 上跑。
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
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

# 系统约定文件：由 01-skill-creator 或本 Skill 的脚手架生成，不要求在 SKILL.md 里被引用
SYSTEM_FILES = {"architecture.md", "maintenance-history.md"}

# evals.json 里每条 eval 必须有的字段（缺一即结构不合规）
EVAL_ROUTES = {"patch", "lean", "system"}

# 只认**本 Skill 内**的引用。负向后顾 (?<![\w\-/]) 用来排掉带 Skill 名前缀的外部路径：
#   `planners-review-core/scripts/inline_review_tokens.py` 里的 `scripts/...` 不是本地文件，
# 不加这个后顾会被误报成 Broken Link（2026-10-16 实测踩到）。
REF_PATTERN = re.compile(r'(?<![\w\-/])(?:references|scripts|assets)/[\w\-./]+')


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


def check_python_syntax(path: Path) -> str | None:
    """内存内编译，返回 None 表示通过，否则返回错误描述。

    不用 py_compile：它会写 .pyc 到用户缓存目录，在沙箱里 PermissionError。
    """
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return None
    except SyntaxError as exc:
        return f"{exc.__class__.__name__}: {exc}"
    except OSError as exc:
        return f"读不出来: {exc}"


def smoke_import(path: Path) -> tuple[str, str | None]:
    """在子进程里 import 这个脚本，抓「语法合法但一导入就炸」这一类错误。

    为什么需要：`py_compile` / `compile()` 只看语法。像 `def f() -> str | None:` 在 3.9 下
    是**合法语法、运行期抛 TypeError**，纯语法检查永远放行。这类缺陷只有真导入才暴露。

    安全性：只在脚本带 `if __name__ == "__main__"` 守卫时做——有守卫时 import 不执行 main()。

    结果分诊（避免把一个会误报的门禁做成「恒真警告」）：
      最后一个栈帧落在**脚本自己**身上 → `self_error`，是脚本缺陷，报 error；
      落在第三方库/环境身上（如 sandbox 里 numba 无缓存目录）→ `env_error`，只报 warning。
    返回 (status, detail)，status ∈ ok / no_guard / self_error / env_error / timeout。
    """
    src = path.read_text(encoding="utf-8")
    if '__name__ == "__main__"' not in src and "__name__ == '__main__'" not in src:
        return "no_guard", None
    code = (
        "import importlib.util, sys;"
        "spec = importlib.util.spec_from_file_location('probe', sys.argv[1]);"
        "mod = importlib.util.module_from_spec(spec);"
        "spec.loader.exec_module(mod)"
    )
    try:
        r = subprocess.run([sys.executable, "-c", code, str(path)],
                           capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return "timeout", "导入超时（>30s）"
    if r.returncode == 0:
        return "ok", None
    err = r.stderr or ""
    tail = [ln for ln in err.strip().splitlines() if ln.strip()]
    detail = tail[-1] if tail else f"exit {r.returncode}"
    frames = re.findall(r'File "([^"]+)"', err)
    status = "self_error" if frames and frames[-1] == str(path) else "env_error"
    return status, detail



def _sibling_skill_roots(skill_dir: Path) -> list[Path]:
    """同一个 skills 库里的兄弟 Skill 根目录（跨 Skill 引用要在那里找）。

    目录有两种形状：库根下面是**分类目录**（`03-design-delivery/video-craft`），
    分类目录下面是**Skill 目录**。所以每一级都要同时看「子目录里有 SKILL.md」（本身是 Skill）
    与「孙目录里有 SKILL.md」（子目录是分类）。取各级里找得最多的那一份当答案——
    库根一定比某一层分类目录找得多。跳过 `_archive`：指向归档的引用不该算有效。
    """
    best: list[Path] = []
    for parent in skill_dir.parents:
        roots: list[Path] = []
        try:
            children = list(parent.iterdir())
        except OSError:
            continue
        for child in children:
            if not child.is_dir() or child.name.startswith(("_", ".")):
                continue
            try:
                if (child / "SKILL.md").is_file():
                    roots.append(child)
                    continue
                roots += [g for g in child.iterdir()
                          if g.is_dir() and not g.name.startswith(("_", "."))
                          and (g / "SKILL.md").is_file()]
            except OSError:
                continue
        roots = [r for r in roots if r != skill_dir]
        if len(roots) > len(best):
            best = roots
    return best

def lint_skill(skill_path_str):
    skill_dir = Path(skill_path_str).resolve()
    if not skill_dir.is_dir():
        print(f"{RED}[ERROR] 路径不是一个目录: {skill_dir}{RESET}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    passes: list[str] = []

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
    # 只是**词汇命中**：正文提到了这些维度，不代表 3+1 真的分开了。
    # 曾经把它写成 [PASS] "包含 3+1 架构要素"，读起来像架构已通过 —— 那正是
    # 「退出码 0 不能当架构通过」的一个来源。真正判结构的是下面第 9 条。
    hit = [label for label, keys in keywords_3plus1.items()
           if any(k.lower() in skill_content.lower() for k in keys)]
    if len(hit) == len(keywords_3plus1):
        passes.append(f"SKILL.md 的正文覆盖了 3+1 的四个维度（词汇命中，非结构判据）")
    else:
        warnings.append(f"SKILL.md 正文没有覆盖这些维度：{sorted(set(keywords_3plus1) - set(hit))}")

    # 3. 内部引用完整性 (Broken Links)
    # 扫描面 = SKILL.md + 所有 references/*.md（维护历史除外：它按定义记录已删文件）
    ref_dir = skill_dir / "references"
    found_refs = set(REF_PATTERN.findall(skill_content))
    if ref_dir.exists():
        for r_file in sorted(ref_dir.rglob("*.md")):
            if r_file.name == "maintenance-history.md":
                continue
            found_refs.update(REF_PATTERN.findall(r_file.read_text(encoding="utf-8")))

    # 引用分三类，别把三类都当错：
    #   ① 本 Skill 内存在            → 有效
    #   ② 别的 Skill 里有同名路径     → 跨 Skill 引用，有效（文档本来就常指向兄弟 Skill）
    #   ③ 哪里都没有                 → `references/`+`scripts/` 属失效链接（错）；
    #                                  `assets/` 多为文档里的示例资产名（警告即可）
    # 不这么分的话，video-craft 那种大 Skill 一跑就是 9 条误报，门禁直接被无视。
    siblings = _sibling_skill_roots(skill_dir)
    for ref in sorted(found_refs):
        if (skill_dir / ref).exists():
            passes.append(f"有效引用: {ref}")
            continue
        hit = next((root.name for root in siblings if (root / ref).exists()), None)
        if hit:
            passes.append(f"跨 Skill 引用: {ref}（在 {hit} 里）")
        elif ref.startswith("assets/"):
            warnings.append(f"引用的资产不存在（文档里可能是示例名）: '{ref}'")
        else:
            errors.append(f"失效的文件引用 (Broken Link): 引用了 '{ref}'，但文件不存在")

    # 4. 孤儿文件检查 (Sediment 检查)
    # 原实现只扫 references/*.md，于是 assets/ 与 scripts/ 里的真孤儿（谁都不引用）扫不到。
    # 现在按目录扫全量：references/ 下的 md、assets/ 下的任何文件、scripts/ 下的 py。
    corpus = [skill_content] + [
        p.read_text(encoding="utf-8")
        for p in (sorted(ref_dir.rglob("*.md")) if ref_dir.exists() else [])
        if p.name != "maintenance-history.md"
    ]

    def referenced(rel: str) -> bool:
        """路径或**裸文件名**任一生效即算被引用 —— 文档里通常写 `render.py` 而不是全路径。"""
        name = Path(rel).name
        return any(rel in text or name in text for text in corpus)

    # 目录名不写死：工具住哪儿是 Skill 自己的事。实测 video-craft 的 55 个脚本在
    # `helpers/`、7 个在 `visual/scripts/`，而早期版本只扫 references/assets/scripts，
    # 于是一个孤儿都报不出来 —— 那盏绿灯因此是假的。
    CODE_SUFFIXES = {".py", ".mjs", ".js", ".sh", ".ts"}
    # 这些目录里的文件不要求被文档引用：
    #   tests/   —— 它是判据的**可执行形态**，没有哪份文档该逐条引用测试名
    #   archive/ —— 架构说明写明它是「为什么是现在这样」的证据，只读
    #   lib/     —— 随附/安装用的第三方件
    SKIP_DIRS = {"__pycache__", "node_modules", ".git", ".venv",
                 "archive", "tests", "lib"}
    orphan_scan: list[tuple[str, bool]] = []
    for sub in sorted(p for p in skill_dir.iterdir() if p.is_dir()):
        if sub.name.startswith(".") or sub.name in SKIP_DIRS:
            continue
        if not (sub.name in ("references", "assets") or sub.name in ("scripts", "helpers")
                or any(q.suffix in CODE_SUFFIXES for q in sub.rglob("*") if q.is_file())):
            continue
        for q in sorted(sub.rglob("*")):
            if not q.is_file() or any(part in SKIP_DIRS for part in q.parts):
                continue
            if q.suffix not in CODE_SUFFIXES and sub.name not in ("references", "assets"):
                continue
            # 下划线开头 = 私有模块约定（被别的 helper import，不对外）；lint 工具自己同理
            exempt = (q.name in SYSTEM_FILES or q.name == "lint_skill.py"
                      or q.name.startswith("_") or "lib" in q.parts)
            orphan_scan.append((str(q.relative_to(skill_dir)), exempt))

    for rel, exempt in orphan_scan:
        if exempt or referenced(rel):
            continue
        warnings.append(f"孤儿文件 (没有任何 SKILL.md/references 引用，可能属于历史沉积 Sediment): {rel}")

    scripts_dir = skill_dir / "scripts"

    # 5. 检查 references/architecture.md 是否存在
    arch_md = skill_dir / "references" / "architecture.md"
    if not arch_md.exists():
        warnings.append("缺少系统架构说明书: references/architecture.md (深模块与所有权规范推荐具备)")
    else:
        passes.append("具备系统架构说明书: references/architecture.md")

    # 6. 检查 scripts/ 脚本：内存内编译（不落盘）+ 能安全导入时的导入冒烟
    if scripts_dir.exists():
        for py_script in sorted(scripts_dir.glob("*.py")):
            err = check_python_syntax(py_script)
            if err:
                errors.append(f"Python 脚本存在语法错误: scripts/{py_script.name} -> {err}")
                continue
            passes.append(f"Python 脚本语法合法: scripts/{py_script.name}")
            smoke_status, smoke_detail = smoke_import(py_script)
            if smoke_status == "ok":
                passes.append(f"Python 脚本导入冒烟通过: scripts/{py_script.name}")
            elif smoke_status == "no_guard":
                warnings.append(
                    f"scripts/{py_script.name} 缺 `if __name__ == \"__main__\"` 守卫："
                    f"被 import 时会直接执行，无法安全做导入冒烟")
            elif smoke_status == "self_error":
                errors.append(f"Python 脚本导入即失败（语法过但运行期炸）: "
                              f"scripts/{py_script.name} -> {smoke_detail}")
            else:
                # 栈帧落在第三方库/环境上：不是脚本的缺陷，别误报成 error
                warnings.append(f"scripts/{py_script.name} 导入冒烟未能完成（依赖或环境问题，非脚本缺陷）: "
                                f"{smoke_detail}")

    # 7. evals/ 的结构与指针
    # 设计原则 8（升级必须做减法）要求减法审计覆盖 eval：写了 eval 却没有指针，
    # 等于没有闭环；eval 的 route_expected 是确定性可校验的，缺字段就是空壳。
    evals_file = skill_dir / "evals" / "evals.json"
    if evals_file.exists():
        try:
            blob = json.loads(evals_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"evals/evals.json 不是合法 JSON: {exc}")
            blob = None
        # 两种形状都合法：`{"evals": [...]}` 与**裸数组**。
        # 早期只认前者，于是 video-craft 那份裸数组（1 条、还是空壳）一条都没被检查到 ——
        # 这就是「lint 退出码 0 不能当架构通过」的一个具体来源。
        evals = blob if isinstance(blob, list) else (blob or {}).get("evals")
        if not isinstance(evals, list) or not evals:
            errors.append("evals/evals.json 里没有非空的用例数组（既不是裸数组，也没有 'evals' 键）")
        else:
            kind = "裸数组" if isinstance(blob, list) else "'evals' 键"
            passes.append(f"evals/evals.json 结构合法（{kind}，{len(evals)} 条）")
            for ev in evals:
                eid = (ev or {}).get("id", "?")
                missing = {"id", "prompt"} - set(ev or {})
                if missing:
                    errors.append(f"eval '{eid}' 缺字段: {sorted(missing)}")
                # 判据字段至少要有一种：没有判据的用例是空壳
                if not ({"must_do", "must_not_do", "expected_behavior_change", "route_expected"}
                        & set(ev or {})):
                    errors.append(f"eval '{eid}' 没有任何判据字段"
                                  "（must_do / must_not_do / expected_behavior_change / route_expected）")
                route = (ev or {}).get("route_expected")
                if route and route not in EVAL_ROUTES:
                    errors.append(f"eval '{eid}' 的 route_expected='{route}' 不在 {sorted(EVAL_ROUTES)} 内")
        # 指针必须是**本 Skill 的** evals/。`planners-review-core/evals/...` 这种别的 Skill 的路径
        # 不能顶替 —— 早期版本被子串匹配骗过，于是「Skill 没指向自己的 eval」这条警告被抵消了。
        if not re.search(r"(?<![\w\-/])evals/", skill_content):
            warnings.append("存在 evals/ 但 SKILL.md 没有指向**本 Skill 的** evals/ "
                            "（别的 Skill 的 evals 路径不算）—— 这套 eval 不会被跑到 (闭环缺失)")

    # 9. 模块主人对账（设计原则 7 的可执行形态）
    #    「被 SKILL.md 当成步骤用的脚本，references/architecture.md 的模块表里必须有它」。
    #    实测 video-craft 有 11 个脚本已被写成流程步骤，模块表却一个字都没提 —— 下一个模型
    #    只能从 SKILL.md 拼出它们的行为，读不到接口与「不做什么」。这条能把它变成可见的。
    if arch_md.exists():
        arch_text = arch_md.read_text(encoding="utf-8")
        # 「当成步骤用」的地方不止 SKILL.md：流程类的 reference（tools.md）也一样。
        # 但别把语料扩到所有 references —— 顺带提一句的脚本会变成误报。
        # 语料 = SKILL.md + 全部 references。收窄到「流程类文档」会漏掉
        # `video-story-handoff.md` 这类把某脚本称为「唯一严格入口」的地方（实测漏 3 个）。
        # 这是 WARN 不是 FAIL：宁可多提一句让下一个模型去看，也不要漏掉真正的主人。
        flow_text = "\n".join([skill_content] + [
            p.read_text(encoding="utf-8") for p in sorted(ref_dir.rglob("*.md"))
            if p.name != "maintenance-history.md"])
        # 「登记了」= 在**模块表的某一行里当主体**（行首那一格出现这个文件名）。
        # 只要求「名字在 architecture.md 里出现过」太宽：实测 live_preview.py 只在文首
        # 另一张表里、snapshot_input.py 只在测试行里，都不算有主人。
        table_rows = []
        m_tbl = re.search(r"(?m)^##\s*2\..*$", arch_text)
        if m_tbl:
            tail = arch_text[m_tbl.end():]
            m_next = re.search(r"(?m)^##\s", tail)
            region = tail[: m_next.start()] if m_next else tail
            for line in region.splitlines():
                if line.lstrip().startswith("|") and line.count("|") >= 3:
                    table_rows.append(line.split("|")[1])
        table_text = "\n".join(table_rows) if table_rows else arch_text
        unregistered = []
        for rel, _exempt in orphan_scan:
            p = Path(rel)
            if p.suffix not in {".py", ".mjs", ".js", ".sh", ".ts"} or p.name.startswith("_"):
                continue
            if "vendor" in p.parts or "lib" in p.parts:
                continue          # 随附的第三方件，主人是上游而不是本 Skill
            if p.name in flow_text and p.name not in table_text:
                unregistered.append(rel)
        if unregistered:
            warnings.append(
                "这些脚本在 SKILL.md 里被当成步骤用，但 references/architecture.md 没有登记"
                "（主人／接口／不做什么）：" + ", ".join(sorted(unregistered)[:14]))

    # 10. No-op 废话检查
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
