import json
import math
import os
import argparse
from collections import Counter
from statistics import median
from typing import Dict, Any, List, Optional, Tuple
from openpyxl import load_workbook


ALGORITHMS = ("mapBased", "tokenBased", "treeBased")

# 输入列：12-14 为 b1 格式相似度 JSON
INPUT_DATA_COLS = (12, 13, 14)

# 输出列：15-17 rm0 MK（即最终趋势结果）
OUTPUT_COLS = (15, 16, 17)

# 不同粒度下的可行算法列表
ALGORITHMS_BY_GRANULARITY = {
    "function": ["mapBased", "tokenBased", "treeBased"],
    "method": ["mapBased", "tokenBased", "treeBased"],
    "class": ["mapBased", "tokenBased"],
}

# 输出列的表头
OUTPUT_HEADERS = {
    15: "MK_fix_D",
    16: "MK_fix_D_t",
    17: "MK_fix_R",
}


def _normal_two_sided_p(z: float) -> float:
    """
    功能：
        根据标准正态分布 Z 值计算双侧 p 值。

    参数：
        z: MK 检验得到的标准化 Z 值。

    返回：
        双侧 p 值。
    """
    return math.erfc(abs(z) / math.sqrt(2.0))


def _calc_mk_for_series(values: List[float]) -> Dict[str, Optional[float]]:
    """
    功能：
        对单个数值序列计算 Mann-Kendall 趋势检验指标。

    参数：
        values: 按版本顺序排列的相似度分数列表。

    返回：
        包含 S、Z、p、Sen's slope、Trend 的字典。
        Trend 不区分显著性，只根据 S 的方向判断。
    """
    n = len(values)

    if n < 2:
        return {
            "S": None,
            "Z": None,
            "p": None,
            "sen_slope": None,
            "trend": "insufficient data",
        }

    s = 0
    slopes = []

    for i in range(n - 1):
        for j in range(i + 1, n):
            diff = values[j] - values[i]

            if diff > 0:
                s += 1
            elif diff < 0:
                s -= 1

            slopes.append(diff / (j - i))

    value_counts = Counter(values)

    tie_sum = 0
    for count in value_counts.values():
        if count > 1:
            tie_sum += count * (count - 1) * (2 * count + 5)

    var_s = (
        n * (n - 1) * (2 * n + 5) - tie_sum
    ) / 18.0

    if var_s == 0:
        z = 0.0
    else:
        if s > 0:
            z = (s - 1) / math.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / math.sqrt(var_s)
        else:
            z = 0.0

    p = _normal_two_sided_p(z)
    sen_slope = median(slopes) if slopes else 0.0

    if s > 0:
        trend = "increasing"
    elif s < 0:
        trend = "decreasing"
    else:
        trend = "no trend"

    return {
        "S": s,
        "Z": z,
        "p": p,
        "sen_slope": sen_slope,
        "trend": trend,
    }


def _is_zero(value: float, eps: float = 1e-12) -> bool:
    """
    功能：
        判断一个数值是否可以视为 0。

    参数：
        value: 待判断数值。
        eps: 浮点误差容忍阈值。

    返回：
        True 表示可以视为 0，否则为 False。
    """
    return abs(value) <= eps


def _remove_edge_zeros_enhanced(
    rank_values: List[float],
    value_scores: List[float],
) -> List[float]:
    """
    功能：
        删除序列两端满足以下任一条件的数据点：
        1. rank 值为 0.0
        2. value（相似度分数）为 0.0

        只在两端连续删除，中间位置不删除。

    参数：
        rank_values: rank 值序列（取负后的排名）。
        value_scores: value 值序列（相似度分数），可能包含 -1.0 哨兵值表示无数据。

    返回：
        删除两端满足条件的数据点后的 rank 序列。
    """
    if len(rank_values) != len(value_scores):
        raise ValueError("rank 和 value 序列长度不一致")

    n = len(rank_values)
    left = 0
    right = n - 1

    # 从左端删除
    while left <= right:
        rank_zero = _is_zero(rank_values[left])
        val_zero = value_scores[left] is not None and _is_zero(value_scores[left])
        if rank_zero or val_zero:
            left += 1
        else:
            break

    # 从右端删除
    while right >= left:
        rank_zero = _is_zero(rank_values[right])
        val_zero = value_scores[right] is not None and _is_zero(value_scores[right])
        if rank_zero or val_zero:
            right -= 1
        else:
            break

    return rank_values[left:right + 1]


def _get_nested_field(algorithm_data: Any, field: str) -> Optional[float]:
    """
    功能：
        从 b1 格式嵌套 dict 或旧格式扁平值中提取指定字段。

        b1 格式：
            {"value": 0.85, "rank": -13.0, "total": 38}
        旧格式（仅 rank）：
            -13.0

    参数：
        algorithm_data: 算法对应的数据，可能是 dict 或数值。
        field: 要提取的字段名，'rank' 或 'value'。

    返回：
        提取到的 float 值；若不存在或无法转换则返回 None。
    """
    if algorithm_data is None:
        return None

    if isinstance(algorithm_data, dict):
        val = algorithm_data.get(field)
        if val is None:
            return None
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    # 旧格式：扁平值，只有 'rank' 有意义
    if field == 'rank':
        try:
            return float(algorithm_data)
        except (TypeError, ValueError):
            return None

    return None


def _parse_cell_json(cell_value: Any) -> Optional[Dict[str, Any]]:
    """
    功能：
        解析 Excel 单元格中的 JSON 字符串。

    参数：
        cell_value: 单元格原始值。

    返回：
        解析后的 dict；如果为空则返回 None。
    """
    if cell_value is None:
        return None

    if isinstance(cell_value, dict):
        return cell_value

    text = str(cell_value).strip()

    if not text:
        return None

    return json.loads(text)


def _extract_algorithm_values(
    data: Dict[str, Any],
    algorithm: str,
    remove_edge_zero: bool = True,
    skip_missing: bool = True,
) -> List[float]:
    """
    功能：
        按 data["order"] 顺序提取某一个算法的 rank 序列，并删除两端 rank=0.0 或 value=0.0 的数据点。

    参数：
        data: 单元格中的 JSON 数据（b1 格式或旧格式）。
        algorithm: 算法名称，如 mapBased、tokenBased、treeBased。
        remove_edge_zero:
            True 表示删除该算法序列两端 rank=0.0 或 value=0.0 的数据点。
        skip_missing:
            True 表示缺失版本对或缺失算法值时跳过。

    返回：
        按版本顺序排列、删除两端零值后的 rank 数值序列。
    """
    order = data.get("order", [])

    if not isinstance(order, list) or not order:
        if skip_missing:
            return []
        raise ValueError("data 中缺少有效的 order 字段")

    rank_values = []
    value_scores: List[float] = []

    for version_pair in order:
        item = data.get(version_pair)

        if item is None:
            if skip_missing:
                continue
            raise KeyError(f"缺少版本对数据: {version_pair}")

        alg_data = item.get(algorithm)

        if alg_data is None:
            if skip_missing:
                continue
            raise KeyError(f"版本对 {version_pair} 缺少算法结果: {algorithm}")

        rank = _get_nested_field(alg_data, 'rank')
        if rank is None:
            if skip_missing:
                continue
            raise ValueError(f"版本对 {version_pair} 算法 {algorithm} rank 无效")

        rank_values.append(rank)

        val = _get_nested_field(alg_data, 'value')
        # value 为 None 时（插值点无真实 value），哨兵值设为 -1.0 避免被误删
        value_scores.append(val if val is not None else -1.0)

    if remove_edge_zero:
        rank_values = _remove_edge_zeros_enhanced(rank_values, value_scores)

    return rank_values


def calc_mk_trend_metrics(
    data: Dict[str, Any],
    algorithms: Optional[List[str]] = None,
    skip_missing: bool = True,
) -> Dict[str, Dict[str, Optional[float]]]:
    """
    功能：
        对一个单元格中的版本对相似度结果进行 MK 趋势分析（rm0：先删除两端零值）。
        只分析 algorithms 参数中指定的算法。

    参数：
        data: 单元格中的 JSON 数据。
        algorithms: 需要计算的算法名称列表。None 表示使用全部三个算法。
        skip_missing:
            True 表示缺失数据时跳过。

    返回：
        各算法对应的 MK 指标。
    """
    if algorithms is None:
        algorithms = list(ALGORITHMS)

    results = {}

    for algorithm in algorithms:
        values = _extract_algorithm_values(
            data=data,
            algorithm=algorithm,
            remove_edge_zero=True,
            skip_missing=skip_missing,
        )

        results[algorithm] = _calc_mk_for_series(values)

    return results


def _metrics_to_cell_text(metrics: Dict[str, Any]) -> str:
    """
    功能：
        将 MK 指标字典转换为适合写入 Excel 单元格的 JSON 字符串。

    参数：
        metrics: MK 指标结果。

    返回：
        JSON 字符串。
    """
    return json.dumps(metrics, ensure_ascii=False)


def process_excel_mk_trend(
    input_excel: str,
    output_excel: str,
    algorithms: List[str],
    skip_invalid_cell: bool = True,
) -> None:
    """
    功能：
        读取 Excel 文件，逐表页、逐行处理第 12-14 列（b1 格式的相似度 JSON 数据）。
        第 15-17 列写入删除两端零值后的 MK 趋势分析结果（rm0）。

    参数：
        input_excel: 输入 Excel 文件路径。
        output_excel: 输出 Excel 文件路径。
        algorithms: 需要分析的算法名列表（由粒度决定）。
        skip_invalid_cell:
            True 表示某个单元格为空或 JSON 解析失败时跳过并置空。

    返回：
        None。结果保存到 output_excel。
    """
    wb = load_workbook(input_excel)

    for ws in wb.worksheets:
        # 写入输出列表头
        for col_idx, header in OUTPUT_HEADERS.items():
            ws.cell(row=1, column=col_idx).value = header

        for row_idx in range(2, ws.max_row + 1):
            for data_col, rm0_col in zip(
                INPUT_DATA_COLS, OUTPUT_COLS
            ):
                raw_data_value = ws.cell(row=row_idx, column=data_col).value

                try:
                    # 解析 JSON 数据
                    data = _parse_cell_json(raw_data_value)

                    if data is None:
                        ws.cell(row=row_idx, column=rm0_col).value = None
                        continue

                    # 计算 rm0 MK（删除两端零值后的趋势）
                    rm0_metrics = calc_mk_trend_metrics(
                        data=data,
                        algorithms=algorithms,
                    )

                    ws.cell(row=row_idx, column=rm0_col).value = _metrics_to_cell_text(rm0_metrics)

                except Exception as e:
                    if not skip_invalid_cell:
                        raise

                    ws.cell(row=row_idx, column=rm0_col).value = None
                    print(
                        f"[WARN] sheet={ws.title}, row={row_idx}, "
                        f"data_col={data_col} 处理失败: {e}"
                    )

    os.makedirs(os.path.dirname(output_excel), exist_ok=True)
    wb.save(output_excel)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mann-Kendall trend analysis for similarity data")
    parser.add_argument("input_excel", type=str, help="Input Excel file path")
    parser.add_argument(
        "--granularity",
        type=str,
        choices=["function", "method", "class"],
        required=True,
        help="API granularity (determines the algorithms to analyze): "
        "function/method -> mapBased+tokenBased+treeBased; class -> mapBased+tokenBased",
    )
    args = parser.parse_args()

    input_excel = args.input_excel
    algorithms = ALGORITHMS_BY_GRANULARITY[args.granularity]

    # 生成输出文件名：保持原名，输出到 mk_analyzed 目录
    input_basename = os.path.basename(input_excel)
    output_basename = input_basename.replace('experiment', 'mk_analyzed')

    # 固定输出目录；在实际环境中请替换为指定的输出路径
    output_dir = "/media/he/Rbench/similarity/data_analyze/trend"
    os.makedirs(output_dir, exist_ok=True)

    output_excel = os.path.join(output_dir, output_basename)

    process_excel_mk_trend(
        input_excel=input_excel,
        output_excel=output_excel,
        algorithms=algorithms,
        skip_invalid_cell=True,
    )

    print(f"Analysis completed. Output saved to: {output_excel}")
