import argparse
import io
import math
import tokenize
from pathlib import Path
from typing import Dict, List, Tuple


IGNORED_TOKEN_TYPES = {
    tokenize.COMMENT,
    tokenize.NL,
    tokenize.NEWLINE,
    tokenize.INDENT,
    tokenize.DEDENT,
    tokenize.ENDMARKER,
}


def read_text_best_effort(py_file: Path) -> str:
    """
    功能：
        使用多种常见编码读取 Python 文件内容。

    参数：
        py_file (Path): Python 文件路径。

    返回：
        str: 文件文本内容。

    异常：
        OSError: 文件读取失败时抛出。
    """
    encodings = ("utf-8", "utf-8-sig", "latin-1")
    last_error: OSError | None = None

    for encoding in encodings:
        try:
            return py_file.read_text(encoding=encoding)
        except OSError as exc:
            last_error = exc

    if last_error is not None:
        raise last_error
    raise OSError(f"无法读取文件: {py_file}")


def count_effective_code_lines(source_text: str) -> int:
    """
    功能：
        统计源码中的有效代码行数（去掉空行与注释行）。

    参数：
        source_text (str): 待统计的 Python 源码文本。

    返回：
        int: 有效代码行数。
    """
    active_lines = set()
    reader = io.StringIO(source_text).readline

    for tok in tokenize.generate_tokens(reader):
        if tok.type in IGNORED_TOKEN_TYPES:
            continue
        active_lines.add(tok.start[0])

    return len(active_lines)


def percentile_thresholds(line_counts: List[int]) -> Dict[str, int]:
    """
    功能：
        计算 60%/70%/80%/90% 分位阈值。

    参数：
        line_counts (List[int]): 各文件有效代码行数列表。

    返回：
        Dict[str, int]: 分位阈值映射，键为百分位字符串，值为行数阈值。
    """
    if not line_counts:
        return {}

    sorted_counts = sorted(line_counts)
    total = len(sorted_counts)
    result: Dict[str, int] = {}

    for percent in (60, 70, 80, 90):
        rank = math.ceil((percent / 100.0) * total)
        idx = max(0, rank - 1)
        result[f"{percent}%"] = sorted_counts[idx]

    return result


def top_rank_line_thresholds(line_counts: List[int]) -> Dict[str, int]:
    """
    功能：
        计算名次行数阈值，包括 max、top_10、top_20 ... top_100。

    参数：
        line_counts (List[int]): 各文件有效代码行数列表。

    返回：
        Dict[str, int]: 名次行数阈值映射。
    """
    if not line_counts:
        result = {"max": 0}
        for rank in range(10, 101, 10):
            result[f"top_{rank}"] = 0
        return result

    sorted_desc = sorted(line_counts, reverse=True)
    total = len(sorted_desc)
    result = {"max": sorted_desc[0]}

    for rank in range(10, 101, 10):
        result[f"top_{rank}"] = sorted_desc[rank - 1] if total >= rank else 0

    return result


def analyze_py_line_counts(target_dir: str | Path) -> Tuple[Dict[str, int], Dict[str, int]]:
    """
    功能：
        统计目标目录下所有 .py 文件的有效代码行数，并计算分位阈值。

    参数：
        target_dir (str | Path): 目标目录路径（仅扫描当前层，不递归）。

    返回：
        Tuple[Dict[str, int], Dict[str, int]]:
            - 第一个字典：60%/70%/80%/90% 分位阈值。
            - 第二个字典：名次行数阈值（max、top_10...top_100）。
    """
    root = Path(target_dir).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise NotADirectoryError(f"目录不存在或不可用: {root}")

    line_counts: List[int] = []
    py_files = sorted(p for p in root.iterdir() if p.is_file() and p.suffix == ".py")

    for py_file in py_files:
        try:
            source_text = read_text_best_effort(py_file)
            lines = count_effective_code_lines(source_text)
            line_counts.append(lines)
        except (OSError, tokenize.TokenError) as exc:
            print(f"[WARN] 跳过文件 {py_file.name}: {exc}")

    thresholds = percentile_thresholds(line_counts)
    top_ranks = top_rank_line_thresholds(line_counts)
    return thresholds, top_ranks


def main() -> None:
    """
    功能：
        命令行入口：输入目录路径，打印分位阈值和名次行数阈值。

    参数：
        无

    返回：
        无
    """
    parser = argparse.ArgumentParser(
        description="统计目录下 .py 文件的有效代码行数（去掉空行和注释行）。"
    )
    parser.add_argument("directory", type=str, help="待统计目录路径（仅当前层，不递归）")
    args = parser.parse_args()

    thresholds, top_ranks = analyze_py_line_counts(args.directory)

    print(f"目录: {Path(args.directory).expanduser().resolve()}")

    print("分位阈值（表示有对应比例的文件行数少于等于该值）:")
    for percent in ("60%", "70%", "80%", "90%"):
        threshold = thresholds.get(percent, 0)
        print(f"  {percent}: {threshold} 行")

    print("名次行数阈值:")
    print(f"  max: {top_ranks.get('max', 0)} 行")
    for rank in range(10, 101, 10):
        key = f"top_{rank}"
        print(f"  {key}: {top_ranks.get(key, 0)} 行")


if __name__ == "__main__":
    main()
