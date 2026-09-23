"""
功能说明：
    从带版本列表的 Excel 中逐用例构建 3 组实验（fix_D / fix_D_t / fix_R）的版本选择文件，
    以便后续相似度排序程序按选择的 query / candidate 版本组合运行。

输入约定：
    - Excel 含多个表页，表页名为库名 libname
    - 每个表页首行为表头
    - 第 1 列为 fqn_D，第 2 列为 fqn_R
    - 第 9/10/11 列分别为以 ',' 分隔的版本号列表：bef_versions / transition_versions / aft_versions

输出约定：
    - 对每一行用例，在 casePath = root/libname/fqn_D-fqn_R/ 下写入 compare_versions.json
    - compare_versions.json 始终包含 3 个实验 key；不满足条件的实验标记 enabled=false 并给出 reason
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import pandas as pd


def parse_versions_cell(cell: Any) -> List[str]:
    """
    功能说明：
        将 Excel 单元格中的版本列表解析为字符串列表。

    参数说明：
        cell:
            Excel 单元格值，可能为 NaN/None/str/number。

    返回说明：
        解析得到的版本列表，保持原顺序，去除空白项。
    """
    if cell is None or pd.isna(cell):
        return []
    text = str(cell).strip()
    if not text:
        return []
    parts = [p.strip() for p in text.split(",")]
    return [p for p in parts if p]


def stable_unique(items: Sequence[str]) -> List[str]:
    """
    功能说明：
        对字符串序列做稳定去重，保留首次出现顺序。

    参数说明：
        items:
            输入序列。

    返回说明：
        去重后的列表。
    """
    seen: Set[str] = set()
    out: List[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def pick_kth_hit_from_end(
    versions: Sequence[str],
    allowed: Set[str],
    k: int,
) -> Tuple[Optional[str], Optional[int]]:
    """
    功能说明：
        从列表末尾向前扫描，仅对命中 allowed 的版本计数，返回倒数第 k 个命中版本及其索引。

    参数说明：
        versions:
            待扫描版本列表（有序）。

        allowed:
            允许集合（例如 D_has_versions 或 R_has_versions）。

        k:
            目标命中序号（从 1 开始）。

    返回说明：
        (version, index)
        - 若不足 k 个命中，返回 (None, None)。
    """
    if k <= 0:
        raise ValueError(f"k 必须 >= 1，当前为：{k}")

    hit_count = 0
    for idx in range(len(versions) - 1, -1, -1):
        v = versions[idx]
        if v in allowed:
            hit_count += 1
            if hit_count == k:
                return v, idx
    return None, None


def pick_kth_hit_from_start(
    versions: Sequence[str],
    allowed: Set[str],
    k: int,
) -> Optional[str]:
    """
    功能说明：
        从列表开头向后扫描，仅对命中 allowed 的版本计数，返回正数第 k 个命中版本。

    参数说明：
        versions:
            待扫描版本列表（有序）。

        allowed:
            允许集合（例如 D_has_versions 或 R_has_versions）。

        k:
            目标命中序号（从 1 开始）。

    返回说明：
        命中版本字符串；若不足 k 个命中返回 None。
    """
    if k <= 0:
        raise ValueError(f"k 必须 >= 1，当前为：{k}")

    hit_count = 0
    for v in versions:
        if v in allowed:
            hit_count += 1
            if hit_count == k:
                return v
    return None


def list_py_stems(dir_path: Path) -> List[str]:
    """
    功能说明：
        列出目录下所有 .py 文件名（不含扩展名）。

    参数说明：
        dir_path:
            目录路径。

    返回说明：
        排序后的 stem 列表；目录不存在则返回空列表。
    """
    if not dir_path.is_dir():
        return []
    return sorted([p.stem for p in dir_path.glob("*.py")], key=lambda s: s)


def list_subdir_names(dir_path: Path) -> List[str]:
    """
    功能说明：
        列出目录下所有一级子目录名称。

    参数说明：
        dir_path:
            目录路径。

    返回说明：
        排序后的子目录名列表；目录不存在则返回空列表。
    """
    if not dir_path.is_dir():
        return []
    return sorted([p.name for p in dir_path.iterdir() if p.is_dir()], key=lambda s: s)


def build_compare_plan_for_case(
    libname: str,
    fqn_D: str,
    fqn_R: str,
    case_path: Path,
    bef_versions: List[str],
    transition_versions: List[str],
    aft_versions: List[str],
    x_fix_d: int,
    x_fix_d_t: int,
    x_fix_r: int,
) -> Dict[str, Any]:
    """
    功能说明：
        针对单个用例构建 compare_versions.json 的内容结构。

    参数说明：
        libname:
            库名（表页名）。

        fqn_D:
            Deprecated API 的 FQN。

        fqn_R:
            Replacement API 的 FQN。

        case_path:
            用例目录路径：root/libname/fqn_D-fqn_R/

        bef_versions / transition_versions / aft_versions:
            三段版本列表（保持 Excel 中顺序）。

        x_fix_d / x_fix_d_t / x_fix_r:
            三个实验的 x 选择参数。

    返回说明：
        compare_versions.json 的可序列化字典。
    """
    d_dir = case_path / fqn_D
    r_candidates_dir = case_path / "R_candidates"

    d_has_versions = list_py_stems(d_dir)
    r_has_versions = list_subdir_names(r_candidates_dir)

    d_set = set(d_has_versions)
    r_set = set(r_has_versions)

    experiments: Dict[str, Any] = {
        "fix_D": {
            "enabled": False,
            "query": None,
            "queries": [],
            "candidate": None,
            "candidates": [],
            "reason": "",
        },
        "fix_D_t": {
            "enabled": False,
            "query": None,
            "queries": [],
            "candidate": None,
            "candidates": [],
            "reason": "",
        },
        "fix_R": {
            "enabled": False,
            "query": None,
            "queries": [],
            "candidate": None,
            "candidates": [],
            "reason": "",
        },
    }

    if not case_path.is_dir():
        experiments["fix_D"]["reason"] = "missing casePath"
        experiments["fix_D_t"]["reason"] = "missing casePath"
        experiments["fix_R"]["reason"] = "missing casePath"
    else:
        if not d_dir.is_dir():
            experiments["fix_D"]["reason"] = "missing fqn_D dir"
            experiments["fix_D_t"]["reason"] = "missing fqn_D dir"
            experiments["fix_R"]["reason"] = "missing fqn_D dir"
        if not r_candidates_dir.is_dir():
            if not experiments["fix_D"]["reason"]:
                experiments["fix_D"]["reason"] = "missing R_candidates dir"
            if not experiments["fix_D_t"]["reason"]:
                experiments["fix_D_t"]["reason"] = "missing R_candidates dir"
            if not experiments["fix_R"]["reason"]:
                experiments["fix_R"]["reason"] = "missing R_candidates dir"

    if case_path.is_dir() and d_dir.is_dir() and r_candidates_dir.is_dir():
        query_fix_d, _ = pick_kth_hit_from_end(bef_versions, d_set, x_fix_d)
        if query_fix_d is None:
            experiments["fix_D"]["enabled"] = False
            experiments["fix_D"]["reason"] = "no query in bef_versions"
        else:
            experiments["fix_D"]["enabled"] = True
            experiments["fix_D"]["query"] = query_fix_d
            experiments["fix_D"]["candidates"] = r_has_versions
            experiments["fix_D"]["reason"] = ""

        if not transition_versions:
            experiments["fix_D_t"]["enabled"] = False
            experiments["fix_D_t"]["reason"] = "transition_versions empty"
        else:
            query_fix_d_t, idx = pick_kth_hit_from_end(transition_versions, d_set, x_fix_d_t)
            if query_fix_d_t is None or idx is None:
                experiments["fix_D_t"]["enabled"] = False
                experiments["fix_D_t"]["reason"] = "no query in transition_versions"
            else:
                candidate_seq = list(transition_versions[idx:]) + list(aft_versions)
                candidate_list = [v for v in candidate_seq if v in r_set]
                candidate_list = stable_unique(candidate_list)
                experiments["fix_D_t"]["enabled"] = True
                experiments["fix_D_t"]["query"] = query_fix_d_t
                experiments["fix_D_t"]["candidates"] = candidate_list
                experiments["fix_D_t"]["reason"] = ""

        fix_r_queries_seq = list(bef_versions) + list(transition_versions)
        fix_r_queries = [v for v in fix_r_queries_seq if v in d_set]
        fix_r_queries = stable_unique(fix_r_queries)
        fix_r_candidate = pick_kth_hit_from_start(aft_versions, r_set, x_fix_r)

        if not fix_r_queries:
            experiments["fix_R"]["enabled"] = False
            experiments["fix_R"]["reason"] = "no queries"
        elif fix_r_candidate is None:
            experiments["fix_R"]["enabled"] = False
            experiments["fix_R"]["reason"] = "no candidate in aft_versions"
        else:
            experiments["fix_R"]["enabled"] = True
            experiments["fix_R"]["queries"] = fix_r_queries
            experiments["fix_R"]["candidate"] = fix_r_candidate
            experiments["fix_R"]["reason"] = ""

    return {
        "schema_version": 2,
        "meta": {
            "lib": libname,
            "case_dirname": f"{fqn_D}-{fqn_R}",
            "fqn_D": fqn_D,
            "fqn_R": fqn_R,
            "x": {
                "fix_D": x_fix_d,
                "fix_D_t": x_fix_d_t,
                "fix_R": x_fix_r,
            },
        },
        "inputs": {
            "bef_versions": bef_versions,
            "transition_versions": transition_versions,
            "aft_versions": aft_versions,
            "D_has_versions": d_has_versions,
            "R_has_versions": r_has_versions,
        },
        "experiments": experiments,
    }


def resolve_x_values(args: argparse.Namespace) -> Tuple[int, int, int]:
    """
    功能说明：
        解析三组实验的 x 参数，支持 --x 作为统一默认值。

    参数说明：
        args:
            argparse 解析结果。

    返回说明：
        (x_fix_d, x_fix_d_t, x_fix_r)
    """
    base_x = int(args.x)
    x_fix_d = int(args.x_fix_d) if args.x_fix_d is not None else base_x
    x_fix_d_t = int(args.x_fix_d_t) if args.x_fix_d_t is not None else base_x
    x_fix_r = int(args.x_fix_r) if args.x_fix_r is not None else base_x

    for name, v in [("x_fix_d", x_fix_d), ("x_fix_d_t", x_fix_d_t), ("x_fix_r", x_fix_r)]:
        if v <= 0:
            raise ValueError(f"{name} 必须 >= 1，当前为：{v}")

    return x_fix_d, x_fix_d_t, x_fix_r


def main() -> None:
    """
    功能说明：
        脚本入口：读取 Excel，逐用例生成 compare_versions.json。

    参数说明：
        通过 argparse 传参：
        - root: 用例根目录
        - excel: 输入 Excel 路径
        - x: 统一默认 x（可被三组独立参数覆盖）
        - x_fix_d / x_fix_d_t / x_fix_r: 三组实验独立 x
        - create_missing_case: casePath 不存在时是否自动创建目录并写入文件
    """
    parser = argparse.ArgumentParser(description="Construct compare versions plans for three experiments")
    parser.add_argument("--root", required=True, type=str, help="用例根目录 root")
    parser.add_argument("--excel", required=True, type=str, help="输入 Excel 文件路径")
    parser.add_argument("--x", type=int, default=1, help="统一默认 x，默认为 1")
    parser.add_argument("--x-fix-d", dest="x_fix_d", type=int, default=None, help="fix_D 实验使用的 x（倒数命中）")
    parser.add_argument("--x-fix-d-t", dest="x_fix_d_t", type=int, default=None, help="fix_D_t 实验使用的 x（倒数命中）")
    parser.add_argument("--x-fix-r", dest="x_fix_r", type=int, default=None, help="fix_R 实验使用的 x（正数命中）")
    parser.add_argument(
        "--create-missing-case",
        action="store_true",
        help="当 casePath 不存在时，自动创建目录并写入 compare_versions.json",
    )
    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    excel_path = Path(args.excel).resolve()

    if not excel_path.is_file():
        raise FileNotFoundError(f"Excel 文件不存在：{excel_path}")

    x_fix_d, x_fix_d_t, x_fix_r = resolve_x_values(args)

    total_rows = 0
    written = 0
    skipped = 0

    with pd.ExcelFile(excel_path) as xls:
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)

            for _, row in df.iterrows():
                total_rows += 1
                fqn_d_cell = row.iloc[0] if len(row) > 0 else None
                fqn_r_cell = row.iloc[1] if len(row) > 1 else None

                if fqn_d_cell is None or pd.isna(fqn_d_cell):
                    continue
                if fqn_r_cell is None or pd.isna(fqn_r_cell):
                    continue

                fqn_d = str(fqn_d_cell).strip()
                fqn_r = str(fqn_r_cell).strip()

                if not fqn_d or not fqn_r:
                    continue

                bef_cell = row.iloc[8] if len(row) > 8 else None
                transition_cell = row.iloc[9] if len(row) > 9 else None
                aft_cell = row.iloc[10] if len(row) > 10 else None

                bef_versions = parse_versions_cell(bef_cell)
                transition_versions = parse_versions_cell(transition_cell)
                aft_versions = parse_versions_cell(aft_cell)

                case_dirname = f"{fqn_d}-{fqn_r}"
                case_path = root_path / sheet_name / case_dirname

                if not case_path.is_dir() and not args.create_missing_case:
                    skipped += 1
                    print(f"[SKIP] casePath not found: {case_path}")
                    continue

                if not case_path.is_dir() and args.create_missing_case:
                    case_path.mkdir(parents=True, exist_ok=True)

                plan = build_compare_plan_for_case(
                    libname=sheet_name,
                    fqn_D=fqn_d,
                    fqn_R=fqn_r,
                    case_path=case_path,
                    bef_versions=bef_versions,
                    transition_versions=transition_versions,
                    aft_versions=aft_versions,
                    x_fix_d=x_fix_d,
                    x_fix_d_t=x_fix_d_t,
                    x_fix_r=x_fix_r,
                )

                out_file = case_path / "compare_versions.json"
                out_file.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
                written += 1

    print(f"Done. total_rows={total_rows}, written={written}, skipped={skipped}")


if __name__ == "__main__":
    main()
