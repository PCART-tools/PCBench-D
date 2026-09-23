import argparse
import ast
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Set

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter


DEFAULT_ALGORITHMS = ("mapBased", "tokenBased", "treeBased")
TARGET_COL_START = 12
TARGET_COL_END = 14


def setup_logger(log_dir: Path) -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        log_dir: 日志文件保存目录
    
    Returns:
        配置好的日志记录器实例
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "analyzed_interpolate.log"

    logger = logging.getLogger("analyzed_interpolate_logger")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def parse_raw_rank_score(rank: Any) -> float:
    """
    读取原始排名值

    Args:
        rank: 排名值

    Returns:
        原始rank值；rank不存在或无法转换时返回0.0
    """
    if rank is None:
        return 0.0

    try:
        return float(rank)
    except (TypeError, ValueError):
        return 0.0


def interpolate_middle_missing_with_indices(
    values: List[Optional[float]],
) -> Tuple[List[float], Set[int]]:
    """
    对中间缺失值进行线性插值
    
    Args:
        values: 包含可能为None的浮点值列表
    
    Returns:
        插值后的浮点值列表和被插值的索引集合
    """
    values = values[:]
    n = len(values)
    interpolated_indices: Set[int] = set()

    i = 0
    while i < n:
        if values[i] is not None:
            i += 1
            continue

        start = i
        while i < n and values[i] is None:
            i += 1
        end = i - 1

        left_idx = start - 1
        right_idx = i

        has_left = left_idx >= 0 and values[left_idx] is not None
        has_right = right_idx < n and values[right_idx] is not None

        if has_left and has_right:
            left_value = values[left_idx]
            right_value = values[right_idx]
            gap_len = end - start + 1

            for offset, pos in enumerate(range(start, end + 1), start=1):
                values[pos] = left_value + (right_value - left_value) * offset / (gap_len + 1)
                interpolated_indices.add(pos)
        else:
            for pos in range(start, end + 1):
                values[pos] = 0.0

    return [float(v) for v in values], interpolated_indices


def build_raw_rank_data(
    data: Dict[str, Any],
    algorithms: Sequence[str] = DEFAULT_ALGORITHMS,
) -> Tuple[Dict[str, Any], Dict[str, Set[str]]]:
    """
    构建归一化的排名数据
    
    Args:
        data: 包含版本对排名信息的字典
        algorithms: 要处理的算法列表
    
    Returns:
        归一化后的数据字典和被插值的版本对集合
    """
    order = list(data.get("order", []))

    result: Dict[str, Any] = {
        "order": order
    }

    for version_pair in order:
        result[version_pair] = {}

    interpolated_versions: Dict[str, Set[str]] = {}

    for alg in algorithms:
        raw_scores: List[Optional[float]] = []

        for version_pair in order:
            item = data.get(version_pair, {})
            exists = bool(item.get("exists", False))

            if not exists:
                raw_scores.append(None)
                continue

            algorithms_data = item.get("algorithms", {})

            if not isinstance(algorithms_data, dict):
                raw_scores.append(0.0)
                continue

            alg_info = algorithms_data.get(alg)

            if not isinstance(alg_info, dict):
                raw_scores.append(0.0)
                continue

            rank = alg_info.get("rank")

            score = parse_raw_rank_score(rank) * -1
            raw_scores.append(score)

        filled_scores, interpolated_indices = interpolate_middle_missing_with_indices(raw_scores)

        for version_pair, score in zip(order, filled_scores):
            result[version_pair][alg] = score

        for idx in interpolated_indices:
            version_pair = order[idx]
            interpolated_versions.setdefault(version_pair, set()).add(alg)

    return result, interpolated_versions


def parse_cell_json(value: Any) -> Optional[Dict[str, Any]]:
    """
    解析单元格中的JSON数据
    
    Args:
        value: 单元格值
    
    Returns:
        解析后的字典，若解析失败则返回None
    """
    if value is None:
        return None

    if isinstance(value, dict):
        return value

    text = str(value).strip()
    if not text or text == "-":
        return None

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(text)
        except Exception:
            return None

    if not isinstance(parsed, dict):
        return None

    if "order" not in parsed:
        return None

    return parsed


def process_excel(input_excel: Path, output_excel: Path, log_dir: Path) -> None:
    """
    处理Excel文件中的版本对排名数据
    
    Args:
        input_excel: 输入Excel文件路径
        output_excel: 输出Excel文件路径
        log_dir: 日志文件保存目录
    """
    logger = setup_logger(log_dir)

    wb = load_workbook(input_excel)

    total_cells = 0
    processed_cells = 0
    skipped_cells = 0
    interpolated_count = 0

    for ws in wb.worksheets:
        sheet_name = ws.title

        for row_idx in range(2, ws.max_row + 1):
            for col_idx in range(TARGET_COL_START, TARGET_COL_END + 1):
                total_cells += 1

                cell = ws.cell(row=row_idx, column=col_idx)
                col_letter = get_column_letter(col_idx)

                raw_data = parse_cell_json(cell.value)

                if raw_data is None:
                    skipped_cells += 1
                    continue

                try:
                    rank_data, interpolated_versions = build_raw_rank_data(raw_data)
                except Exception as exc:
                    skipped_cells += 1
                    logger.exception(
                        "处理失败 | sheet=%s | row=%d | col=%s | error=%s",
                        sheet_name,
                        row_idx,
                        col_letter,
                        exc,
                    )
                    continue

                cell.value = json.dumps(
                    rank_data,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )

                processed_cells += 1

                for version_pair, algorithms in interpolated_versions.items():
                    interpolated_count += 1
                    logger.info(
                        "插值 | sheet=%s | row=%d | col=%s | version=%s | algorithms=%s",
                        sheet_name,
                        row_idx,
                        col_letter,
                        version_pair,
                        ",".join(sorted(algorithms)),
                    )

    output_excel.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_excel)

    logger.info(
        "处理完成 | input=%s | output=%s | total_cells=%d | processed_cells=%d | skipped_cells=%d | interpolated_versions=%d",
        input_excel,
        output_excel,
        total_cells,
        processed_cells,
        skipped_cells,
        interpolated_count,
    )


def main() -> None:
    """
    主函数，处理命令行参数并执行Excel文件处理
    """
    parser = argparse.ArgumentParser(
        description="对 Excel 第 12-14 列中的版本对排名 JSON 提取原始rank，并记录中间版本插值日志。"
    )

    parser.add_argument(
        "input_excel",
        help="输入 Excel 文件路径，例如 input.xlsx",
    )

    args = parser.parse_args()

    input_excel = Path(args.input_excel).resolve()

    # 固定输出目录；在实际环境中请替换为指定的输出路径
    output_dir = Path("/media/he/Rbench/similarity/data_analyze/normalization")
    # 生成输出文件名：将 addinfo 替换为 normalized
    output_stem = input_excel.stem.replace("addinfo", "rank_info")
    output_excel = output_dir / f"{output_stem}{input_excel.suffix}"

    # 日志输出到同一目录
    log_dir = output_dir

    process_excel(input_excel, output_excel, log_dir)


if __name__ == "__main__":
    main()