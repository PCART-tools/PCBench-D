#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 RQ2/split2.0 下 fix_D 中各 case 的 R_candidates/Vi-1 和 Vi 中 .py 文件变化统计。

对 candidates_cause, common_cause, dep_rep 三个类型，分别输出一个 JSON 文件，
包含每个 case 的 9 项统计指标和分组汇总。
"""

import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent / "cases_split"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
TYPES = ["candidates_cause", "common_cause", "dep_rep"]
CONSISTENCIES = ["consistent", "no_consistent"]
GRANULARITIES = ["class", "function", "method"]

STAT_NAMES = [
    "vi1_py_count",
    "vi_py_count",
    "deleted",
    "added",
    "common",
    "identical",
    "changed_in_common",
    "total_changes",
    "change_ratio_vs_vi",
    "change_ratio_vs_vi1",
]


def file_md5(path: Path) -> str:
    """返回文件内容的 MD5 十六进制摘要。"""
    return hashlib.md5(path.read_bytes()).hexdigest()


def get_py_files(dir_path: Path) -> dict[str, Path]:
    """返回目录下所有 .py 文件的 {文件名: 完整路径} 映射。"""
    result = {}
    for p in dir_path.glob("*.py"):
        if p.is_file():
            result[p.name] = p
    return result


def locate_version_dirs(rc_dir: Path) -> tuple[Path | None, Path | None]:
    """在 R_candidates 下定位 Vi-1_* 和 Vi_* 目录（解析 symlink）。

    Returns:
        (vi1_dir, vi_dir): 解析后的真实路径，找不到时为 None。
    """
    vi1_dir = None
    vi_dir = None
    for entry in rc_dir.iterdir():
        if entry.name.startswith("Vi-1"):
            vi1_dir = entry.resolve()
        elif entry.name.startswith("Vi"):
            vi_dir = entry.resolve()
    return vi1_dir, vi_dir


def resolve_case_path(entry: Path) -> Path | None:
    """解析 case 目录、符号链接或 Windows 下保存的相对路径引用文件。"""
    if entry.is_dir() or entry.is_symlink():
        return entry.resolve()
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


def analyze_case(real_path: Path) -> dict | None:
    """分析单个 case 的 R_candidates 变化统计。

    Returns:
        包含 9 项统计的 dict；若目录结构异常返回 None。
    """
    rc_dir = real_path / "R_candidates"
    if not rc_dir.is_dir():
        return None

    vi1_dir, vi_dir = locate_version_dirs(rc_dir)
    if vi1_dir is None or vi_dir is None:
        return None

    vi1_files = get_py_files(vi1_dir)
    vi_files = get_py_files(vi_dir)

    vi1_names = set(vi1_files.keys())
    vi_names = set(vi_files.keys())

    common_names = vi1_names & vi_names
    deleted_names = vi1_names - vi_names
    added_names = vi_names - vi1_names

    # 比较共有文件内容
    identical = 0
    for name in common_names:
        if file_md5(vi1_files[name]) == file_md5(vi_files[name]):
            identical += 1

    vi1_count = len(vi1_files)
    vi_count = len(vi_files)
    common_count = len(common_names)
    changed_in_common = common_count - identical
    deleted_count = len(deleted_names)
    added_count = len(added_names)

    # 总变更数 = 删除 + 新增 + 共有但变更
    total_changes = deleted_count + added_count + changed_in_common

    stats = {
        "vi1_py_count": vi1_count,
        "vi_py_count": vi_count,
        "deleted": deleted_count,
        "added": added_count,
        "common": common_count,
        "identical": identical,
        "changed_in_common": changed_in_common,
        "total_changes": total_changes,
        "change_ratio_vs_vi": round(total_changes / vi_count, 4) if vi_count > 0 else None,
        "change_ratio_vs_vi1": round(total_changes / vi1_count, 4) if vi1_count > 0 else None,
    }
    return stats


def collect_cases(base: Path, type_name: str) -> list[dict]:
    """收集某个 type 下 fix_D 中的所有 case（解析 symlink，去重）。

    Returns:
        列表元素: {"consistency", "granularity", "case_name", "real_path"}
    """
    cases = []
    seen = set()
    type_dir = base / type_name / "fix_D"

    if not type_dir.is_dir():
        print(f"  [WARN] {type_dir} 不存在", file=sys.stderr)
        return cases

    for consistency in CONSISTENCIES:
        for granularity in GRANULARITIES:
            gran_dir = type_dir / consistency / granularity
            if not gran_dir.is_dir():
                continue

            for entry in sorted(gran_dir.iterdir()):
                real_case = resolve_case_path(entry)
                if real_case is None:
                    continue
                if not (real_case / "analysis.md").exists():
                    continue
                if real_case in seen:
                    continue
                seen.add(real_case)
                cases.append({
                    "consistency": consistency,
                    "granularity": granularity,
                    "case_name": entry.name,
                    "real_path": real_case,
                })

    return cases


def compute_summary(cases_data: list[dict]) -> dict:
    """计算所有 case 的 overall 总量汇总及基于总量的变化率。"""
    if not cases_data:
        return {"overall": {"case_count": 0}}

    # 计数类指标直接累加，不能对各 case 的值求平均。
    total_keys = STAT_NAMES[:8]
    overall = {"case_count": len(cases_data)}
    for key in total_keys:
        values = [row[key] for row in cases_data if row.get(key) is not None]
        summary_key = key if key == "total_changes" else f"total_{key}"
        overall[summary_key] = sum(values) if values else 0

    # 变化率使用汇总后的分子和分母计算，而不是各 case 变化率的平均值。
    total_changes = overall["total_changes"]
    total_vi = overall["total_vi_py_count"]
    total_vi1 = overall["total_vi1_py_count"]
    overall["change_ratio_vs_vi"] = round(total_changes / total_vi, 4) if total_vi > 0 else None
    overall["change_ratio_vs_vi1"] = round(total_changes / total_vi1, 4) if total_vi1 > 0 else None

    return {"overall": overall}


def build_type_json(type_name: str, cases_info: list[dict]) -> dict:
    """构建单个 type 的完整 JSON 结构。"""
    cases_data = []
    skipped = 0
    for info in cases_info:
        stats = analyze_case(info["real_path"])
        if stats is None:
            skipped += 1
            print(f"  [SKIP] {info['case_name']}: 缺少 R_candidates 或 Vi 目录")
            continue
        row = {
            "consistency": info["consistency"],
            "granularity": info["granularity"],
            "case_name": info["case_name"],
            **stats,
        }
        cases_data.append(row)

    # meta
    cons_counts = {c: 0 for c in CONSISTENCIES}
    gran_counts = {g: 0 for g in GRANULARITIES}
    for row in cases_data:
        cons_counts[row["consistency"]] += 1
        gran_counts[row["granularity"]] += 1

    meta = {
        "type": type_name,
        "description": "RQ2/split2.0 fix_D: R_candidates Vi-1 vs Vi .py file change statistics",
        "total_cases": len(cases_data),
        "skipped": skipped,
        "consistency": cons_counts,
        "granularity": gran_counts,
    }

    summary = compute_summary(cases_data)

    return {
        "meta": meta,
        "cases": cases_data,
        "summary": summary,
    }


def main():
    for type_name in TYPES:
        print(f"Processing: {type_name}")
        cases_info = collect_cases(BASE, type_name)
        print(f"  Found {len(cases_info)} unique cases")

        result = build_type_json(type_name, cases_info)

        output_path = OUTPUT_DIR / f"{type_name}_rc_py_stats.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"  -> {output_path}")
        print(f"     cases: {result['meta']['total_cases']}, "
              f"skipped: {result['meta']['skipped']}")

    print("\nDone.")


if __name__ == "__main__":
    main()
