"""
功能：
    从指定 root 目录读取版本对的相似度排名结果，并将结果以 JSON 字符串写回 Excel。

数据约定（按列号）：
    - 第 1 列：fqn_D（Deprecated API 的全限定名）
    - 第 2 列：fqn_R（Replacement API 的全限定名）
    - 第 9 列：bef_n_version（逗号分隔的版本列表）
    - 第 10 列：transition（逗号分隔的版本列表）
    - 第 11 列：aft_n_version（逗号分隔的版本列表）
    - 第 12-14 列：脚本生成的 fix_D / fix_D_t / fix_R（JSON 字符串）

目录结构约定：
    root/<libname>/<fqn_D>-<fqn_R>/result/<fix_type>/<version_pair>/
        - mapBased.json
        - tokenBased.json
        - treeBased.json

说明：
    - 本脚本假设 Excel 第 9-11 列中的版本号列表不存在重复，也不存在重叠，因此生成的版本对列表无需再额外去重。
    - 读取 JSON 时遵循“尽可能容错”的策略：文件不存在、无法解析、或格式不符合预期时返回空结果结构。
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from openpyxl import load_workbook


ALGORITHM_FILES = {
    "mapBased": ["mapBased.json"],
    "tokenBased": ["tokenBased.json"],
    "treeBased": ["treeBased.json"],
}

QUERY_API_BY_FIX_TYPE = {
    "fix_D": "D",
    "fix_D_t": "D",
    "fix_R": "R",
}


def cell_to_text(value: Any) -> str:
    """
    功能：
        将 Excel 单元格内容转换为字符串。

    参数：
        value: 单元格原始值。

    返回：
        去除首尾空白后的字符串。
    """
    if value is None:
        return ""

    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return str(value)

    return str(value).strip()


def parse_version_list(value: Any) -> List[str]:
    """
    功能：
        解析以逗号分隔的版本号列表，保持原始顺序。

    参数：
        value: Excel 单元格内容。

    返回：
        版本号列表。空字符串和 '-' 会被忽略。
    """
    text = cell_to_text(value)
    if not text or text == "-":
        return []

    versions = []
    for item in text.split(","):
        item = item.strip()
        if item and item != "-":
            versions.append(item)

    return versions


def build_version_pairs(
    bef_versions: List[str],
    transition_versions: List[str],
    aft_versions: List[str],
) -> Dict[str, List[str]]:
    """
    功能：
        根据 bef_n_version、transition、aft_n_version 构建三类版本对。

    参数：
        bef_versions: 第 11 列解析出的版本列表。
        transition_versions: 第 12 列解析出的版本列表。
        aft_versions: 第 13 列解析出的版本列表。

    返回：
        {
            "fix_D": [...],
            "fix_D_t": [...],
            "fix_R": [...]
        }
    """
    fix_d_pairs = []
    fix_d_t_pairs = []
    fix_r_pairs = []

    if bef_versions:
        source = bef_versions[-1]
        targets = transition_versions + aft_versions
        fix_d_pairs = [f"{source}-{target}" for target in targets]

    if transition_versions:
        source = transition_versions[-1]
        targets = aft_versions
        fix_d_t_pairs = [f"{source}-{target}" for target in targets]

    if aft_versions:
        target = aft_versions[0]
        sources = bef_versions + transition_versions
        fix_r_pairs = [f"{source}-{target}" for source in sources]

    return {
        "fix_D": fix_d_pairs,
        "fix_D_t": fix_d_t_pairs,
        "fix_R": fix_r_pairs,
    }


def find_algorithm_json(pair_dir: Path, algorithm_name: str) -> Optional[Path]:
    """
    功能：
        在版本对目录下查找指定算法的 JSON 文件。

    参数：
        pair_dir: 版本对目录。
        algorithm_name: 算法名称，取值为 mapBased、tokenBased、treeBased。

    返回：
        找到则返回 JSON 文件路径，否则返回 None。
    """
    for filename in ALGORITHM_FILES[algorithm_name]:
        json_path = pair_dir / filename
        if json_path.is_file():
            return json_path

    return None


def read_json_list(json_path: Path) -> List[Dict[str, Any]]:
    """
    功能：
        读取算法结果 JSON 文件，并返回其中的字典元素列表。

    参数：
        json_path: JSON 文件路径。

    返回：
        JSON 列表（仅保留 dict 元素）。读取失败、解析失败或格式不对时返回空列表。
    """
    try:
        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []

    if not isinstance(data, list):
        return []

    return [item for item in data if isinstance(item, dict)]


def extract_algorithm_result(json_path: Path, target_api_name: str) -> Dict[str, Any]:
    """
    功能：
        从单个算法 JSON 文件中提取目标 API 的 score、rank 和 total。

    参数：
        json_path: 算法 JSON 文件路径。
        target_api_name: 需要匹配的 api_name。

    返回：
        {
            "value": score 或 None,
            "rank": rank 或 None,
            "total": JSON 列表长度
        }
    """
    data = read_json_list(json_path)
    total = len(data)

    for item in data:
        if cell_to_text(item.get("api_name")) == target_api_name:
            return {
                "value": item.get("score"),
                "rank": item.get("rank"),
                "total": total,
            }

    return {
        "value": None,
        "rank": None,
        "total": total,
    }


def empty_pair_result() -> Dict[str, Any]:
    """
    功能：
        构建版本对不存在时的空结果结构。

    参数：
        无。

    返回：
        空版本对结果。
    """
    return {
        "exists": False,
        "algorithms": {
            "mapBased": None,
            "tokenBased": None,
            "treeBased": None,
        },
    }


def read_pair_result(pair_dir: Path, target_api_name: str) -> Dict[str, Any]:
    """
    功能：
        读取一个版本对目录下三种算法的结果。

    参数：
        pair_dir: 版本对目录。
        target_api_name: 需要匹配的 api_name。

    返回：
        单个版本对的结果结构。
    """
    if not pair_dir.is_dir():
        return empty_pair_result()

    algorithms = {}

    for algorithm_name in ["mapBased", "tokenBased", "treeBased"]:
        json_path = find_algorithm_json(pair_dir, algorithm_name)

        if json_path is None:
            algorithms[algorithm_name] = None
        else:
            algorithms[algorithm_name] = extract_algorithm_result(
                json_path=json_path,
                target_api_name=target_api_name,
            )

    return {
        "exists": True,
        "algorithms": algorithms,
    }


def build_fix_result_json(
    root: Path,
    libname: str,
    fqn_d: str,
    fqn_r: str,
    fix_type: str,
    version_pairs: List[str],
) -> Dict[str, Any]:
    """
    功能：
        构建 fix_D、fix_D_t 或 fix_R 对应的完整 JSON 结构。

    参数：
        root: 根目录。
        libname: 当前表页名。
        fqn_d: 第 1 列 fqn_D。
        fqn_r: 第 2 列 fqn_R。
        fix_type: fix_D、fix_D_t 或 fix_R。
        version_pairs: 需要识别的版本对列表。

    返回：
        可写入 Excel 单元格的 JSON 对象。
    """
    result = {
        "order": version_pairs,
    }

    # 三类 fix 都统一在算法 JSON 中匹配 fqn_R
    target_api_name = fqn_r

    base_dir = root / libname / f"{fqn_d}-{fqn_r}" / "result" / fix_type

    for pair_name in version_pairs:
        pair_dir = base_dir / pair_name
        result[pair_name] = read_pair_result(
            pair_dir=pair_dir,
            target_api_name=target_api_name,
        )

    return result


def json_to_cell_text(data: Dict[str, Any]) -> str:
    """
    功能：
        将 JSON 对象转换为适合写入 Excel 单元格的字符串。

    参数：
        data: JSON 对象。

    返回：
        JSON 字符串（UTF-8，可包含中文；无额外空格，便于单元格存储与后续解析）。
    """
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def process_workbook(excel_path: Path, root: Path, output_path: Path) -> None:
    """
    功能：
        处理整个 Excel 文件，逐表页、逐行生成 fix_D、fix_D_t、fix_R 三列。

    参数：
        excel_path: 输入 Excel 路径。
        root: 数据根目录。
        output_path: 输出 Excel 路径。
    """
    wb = load_workbook(excel_path)

    for ws in wb.worksheets:
        libname = ws.title

        ws.cell(row=1, column=12).value = "fix_D"
        ws.cell(row=1, column=13).value = "fix_D_t"
        ws.cell(row=1, column=14).value = "fix_R"

        for row_idx in range(2, ws.max_row + 1):
            fqn_d = cell_to_text(ws.cell(row=row_idx, column=1).value)
            fqn_r = cell_to_text(ws.cell(row=row_idx, column=2).value)

            if not fqn_d or not fqn_r:
                ws.cell(row=row_idx, column=12).value = json_to_cell_text({"order": []})
                ws.cell(row=row_idx, column=13).value = json_to_cell_text({"order": []})
                ws.cell(row=row_idx, column=14).value = json_to_cell_text({"order": []})
                continue

            bef_versions = parse_version_list(ws.cell(row=row_idx, column=9).value)
            transition_versions = parse_version_list(ws.cell(row=row_idx, column=10).value)
            aft_versions = parse_version_list(ws.cell(row=row_idx, column=11).value)

            pair_map = build_version_pairs(
                bef_versions=bef_versions,
                transition_versions=transition_versions,
                aft_versions=aft_versions,
            )

            fix_d_result = build_fix_result_json(
                root=root,
                libname=libname,
                fqn_d=fqn_d,
                fqn_r=fqn_r,
                fix_type="fix_D",
                version_pairs=pair_map["fix_D"],
            )

            fix_d_t_result = build_fix_result_json(
                root=root,
                libname=libname,
                fqn_d=fqn_d,
                fqn_r=fqn_r,
                fix_type="fix_D_t",
                version_pairs=pair_map["fix_D_t"],
            )

            fix_r_result = build_fix_result_json(
                root=root,
                libname=libname,
                fqn_d=fqn_d,
                fqn_r=fqn_r,
                fix_type="fix_R",
                version_pairs=pair_map["fix_R"],
            )

            ws.cell(row=row_idx, column=12).value = json_to_cell_text(fix_d_result)
            ws.cell(row=row_idx, column=13).value = json_to_cell_text(fix_d_t_result)
            ws.cell(row=row_idx, column=14).value = json_to_cell_text(fix_r_result)

    wb.save(output_path)


def parse_args() -> argparse.Namespace:
    """
    功能：
        解析命令行参数。

    参数：
        无。

    返回：
        argparse.Namespace。
    """
    parser = argparse.ArgumentParser(
        description="从指定 root 目录读取版本对排名结果，并写入 Excel 第 12-14 列。"
    )

    parser.add_argument(
        "excel",
        type=str,
        help="输入 Excel 文件路径。",
    )

    parser.add_argument(
        "root",
        type=str,
        help="结果数据根目录。",
    )

    return parser.parse_args()


def main() -> None:
    """
    功能：
        命令行入口：解析参数并执行 Excel 处理流程。

    参数：
        无。

    返回：
        无。
    """
    args = parse_args()

    excel_path = Path(args.excel).resolve()
    root = Path(args.root).resolve()

    output_dir = Path(__file__).resolve().parent / "raw_data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = (output_dir / f"{excel_path.stem}_addinfo{excel_path.suffix}").resolve()

    process_workbook(
        excel_path=excel_path,
        root=root,
        output_path=output_path,
    )

    print(f"处理完成：{output_path}")


if __name__ == "__main__":
    main()
