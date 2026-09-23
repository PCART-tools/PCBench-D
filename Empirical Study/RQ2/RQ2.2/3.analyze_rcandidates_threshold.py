#!/usr/bin/env python3
"""统计各 fix_D 目录下 R_candidates 的 .py 文件变化是否达到 10% 阈值。

Vi-1 → Vi 的 .py 文件数量变化率 = |Vi.py - Vi-1.py| / Vi-1.py
判断是否 >= 10%。
"""

import os
import json
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent / "cases_split"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

TARGETS = [
    ("candidates_cause", "consistent"),
    ("candidates_cause", "no_consistent"),
    ("common_cause", "consistent"),
    ("common_cause", "no_consistent"),
    ("dep_rep", "consistent"),
    ("dep_rep", "no_consistent"),
]

GRANULARITIES = ["class", "function", "method"]


def count_py_files(directory: Path) -> int:
    """递归统计目录下 .py 文件数量（跟随软链接）。"""
    if not directory.exists():
        return 0
    count = 0
    for root, dirs, files in os.walk(directory, followlinks=True):
        for f in files:
            if f.endswith(".py"):
                count += 1
    return count


def resolve_case_path(entry: Path) -> Path | None:
    """解析 case 目录、符号链接或 Windows 下保存的相对路径引用文件。"""
    if entry.is_dir() or entry.is_symlink():
        return entry
    if entry.is_file():
        try:
            target = entry.read_text(encoding="utf-8").strip()
        except OSError:
            return None
        if not target:
            return None
        target_path = (entry.parent / target).resolve()
        if target_path.is_dir():
            return target_path
    return None


def analyze_case(case_dir: Path) -> dict | None:
    """分析单个 case，返回统计信息。"""
    rc_dir = case_dir / "R_candidates"
    if not rc_dir.exists():
        return None

    # 找到 Vi-1 和 Vi 目录（软链接，命名格式 Vi-1_xxx 和 Vi_xxx）
    vi_minus_1_dir = None
    vi_dir = None
    for entry in rc_dir.iterdir():
        if entry.is_symlink() or entry.is_dir():
            if entry.name.startswith("Vi-1"):
                vi_minus_1_dir = entry
            elif entry.name.startswith("Vi"):
                vi_dir = entry

    if not vi_minus_1_dir or not vi_dir:
        return None

    vi1_count = count_py_files(vi_minus_1_dir)
    vi_count = count_py_files(vi_dir)

    if vi1_count == 0:
        return None

    change = vi_count - vi1_count
    change_rate = change / vi1_count

    return {
        "vi1_py": vi1_count,
        "vi_py": vi_count,
        "change": change,
        "change_rate": change_rate,
        "exceeds_10pct": abs(change_rate) >= 0.10,
    }


def main():
    results = {}

    for cause, consist in TARGETS:
        key = f"{cause}/fix_D/{consist}"
        target_dir = BASE / cause / "fix_D" / consist
        total = 0
        exceed = 0
        details = []

        for gran in GRANULARITIES:
            gran_dir = target_dir / gran
            if not gran_dir.exists():
                continue
            for entry in sorted(gran_dir.iterdir()):
                case_path = resolve_case_path(entry)
                if case_path is None:
                    continue
                case_name = entry.name
                result = analyze_case(case_path)
                if result is None:
                    continue
                total += 1
                if result["exceeds_10pct"]:
                    exceed += 1
                result["case_name"] = case_name
                result["granularity"] = gran
                details.append(result)

        pct = (exceed / total * 100) if total > 0 else 0
        results[key] = {
            "total": total,
            "exceed": exceed,
            "pct": pct,
            "details": details,
        }
        print(f"{key}: {total} cases, {exceed} >=10% ({pct:.1f}%)")

    # 输出 JSON 供后续使用
    output = {}
    for key, val in results.items():
        output[key] = {
            "total": val["total"],
            "exceed": val["exceed"],
            "pct": round(val["pct"], 1),
        }

    print("\n--- Summary ---")
    print(json.dumps(output, indent=2, ensure_ascii=False))

    # 保存详细结果
    detail_output = {}
    for key, val in results.items():
        detail_output[key] = {
            "total": val["total"],
            "exceed": val["exceed"],
            "pct": round(val["pct"], 1),
            "details": [
                {
                    "case": d["case_name"],
                    "granularity": d["granularity"],
                    "vi1_py": d["vi1_py"],
                    "vi_py": d["vi_py"],
                    "change": d["change"],
                    "change_rate": round(d["change_rate"], 4),
                    "exceeds_10pct": d["exceeds_10pct"],
                }
                for d in val["details"]
            ],
        }

    detail_path = OUTPUT_DIR / "R_candidates_threshold_details.json"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(detail_path, "w", encoding="utf-8") as f:
        json.dump(detail_output, f, indent=2, ensure_ascii=False)
    print(f"\nDetails saved to {detail_path}")


if __name__ == "__main__":
    main()
