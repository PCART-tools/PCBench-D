import argparse
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from py_line_stats import (
    analyze_py_line_counts,
    count_effective_code_lines,
    read_text_best_effort,
)


def iter_subdirs(root: Path) -> Iterable[Path]:
    for p in sorted(root.iterdir()):
        if p.is_dir():
            yield p


def iter_py_files(root: Path) -> Iterable[Path]:
    for p in sorted(root.iterdir()):
        if p.is_file() and p.suffix == ".py":
            yield p


def unique_destination_path(dst_dir: Path, file_name: str) -> Path:
    dst = dst_dir / file_name
    if not dst.exists():
        return dst

    src = Path(file_name)
    for i in range(1, 10_000):
        candidate = dst_dir / f"{src.stem}__dup{i}{src.suffix}"
        if not candidate.exists():
            return candidate

    raise RuntimeError(f"目标目录存在过多同名文件，无法生成唯一文件名: {dst_dir}/{file_name}")


def compute_moved_stats(moved_items: List[Tuple[Path, int]]) -> Tuple[int, int, float]:
    if not moved_items:
        return 0, 0, 0.0

    counts = [c for _, c in moved_items]
    return len(counts), min(counts), sum(counts) / len(counts)


def append_del_log(
    del_log: Path,
    version: str,
    p60: int,
    p80: int,
    p90: int,
    move_threshold: int,
    moved_count: int,
    min_lines: int,
    avg_lines: float,
) -> None:
    del_log.parent.mkdir(parents=True, exist_ok=True)
    line = (
        f"{version} | p60={p60} | p80={p80} | p90={p90} | thr={move_threshold} | "
        f"moved={moved_count} | min={min_lines} | avg={avg_lines:.2f}\n"
    )
    with del_log.open("a", encoding="utf-8", errors="strict") as f:
        f.write(line)


def summary_file_path(root_dir: Path) -> Path:
    # 汇总文件保存在输入的 root 路径下，文件名固定为 del_candidates_summary.log
    return root_dir / "del_candidates_summary.log"


def parse_moved_count(del_log_line: str) -> int:
    parts = [p.strip() for p in del_log_line.strip().split("|")]
    for part in parts:
        if part.startswith("moved="):
            try:
                return int(part.split("=", 1)[1])
            except ValueError:
                return 0
    return 0


def build_summary_from_existing_del_logs(root: Path) -> List[str]:
    summary_lines: List[str] = []

    for lib_dir in iter_subdirs(root):
        for case_dir in iter_subdirs(lib_dir):
            del_log = case_dir / "del_candidates" / "del.log"
            if not del_log.is_file():
                continue

            try:
                raw = del_log.read_text(encoding="utf-8")
            except OSError:
                continue

            for line in raw.splitlines():
                if not line.strip():
                    continue
                moved = parse_moved_count(line)
                if moved > 0:
                    summary_lines.append(f"{lib_dir.name} | {case_dir.name} | {line.strip()}\n")

    return summary_lines


def clean_large_candidates(root_dir: str | Path) -> None:
    """
    功能：
        遍历 root/libname/case/R_candidates/version 结构，按版本目录统计有效代码行数分位数，
        将超过阈值的候选 .py 文件移动到 case/del_candidates/<version>/ 下，
        同时在 case/del_candidates/del.log 中记录每个 version 的阈值与移动统计。

        阈值规则：
            thr = max(p90 * 5, p60 * 10, 1000)

        日志格式（每个 version 一行）：
            version | p60=... | p80=... | p90=... | thr=... | moved=... | min=... | avg=...

        汇总输出：
            扫描 root 下所有 case 的 del_candidates/del.log，汇总 moved>0 的行，
            写入 root/del_candidates_summary.log，并在每行前补充 libname 与 case。

    参数：
        root_dir (str | Path): 根目录路径。

    返回：
        无
    """
    root = Path(root_dir).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise NotADirectoryError(f"目录不存在或不可用: {root}")

    for lib_dir in iter_subdirs(root):
        for case_dir in iter_subdirs(lib_dir):
            r_candidates_dir = case_dir / "R_candidates"
            if not r_candidates_dir.is_dir():
                continue

            print(f"processing: {lib_dir.name}/{case_dir.name}")

            del_root = case_dir / "del_candidates"
            del_log = del_root / "del.log"

            for version_dir in iter_subdirs(r_candidates_dir):
                thresholds, _top_ranks = analyze_py_line_counts(version_dir)
                p60 = int(thresholds.get("60%", 0) or 0)
                p80 = int(thresholds.get("80%", 0) or 0)
                p90 = int(thresholds.get("90%", 0) or 0)
                move_threshold = max(p90 * 5, p60 * 10, 1000)
                moved_items: List[Tuple[Path, int]] = []

                for py_file in iter_py_files(version_dir):
                    try:
                        source_text = read_text_best_effort(py_file)
                        lines = count_effective_code_lines(source_text)
                    except Exception as exc:
                        print(f"[WARN] 跳过文件 {py_file}: {exc}")
                        continue

                    if lines > move_threshold:
                        moved_items.append((py_file, lines))

                if moved_items:
                    dst_version_dir = del_root / version_dir.name
                    dst_version_dir.mkdir(parents=True, exist_ok=True)
                    for py_file, _lines in moved_items:
                        dst = unique_destination_path(dst_version_dir, py_file.name)
                        py_file.rename(dst)

                moved_count, min_lines, avg_lines = compute_moved_stats(moved_items)
                append_del_log(
                    del_log,
                    version_dir.name,
                    p60,
                    p80,
                    p90,
                    move_threshold,
                    moved_count,
                    min_lines,
                    avg_lines,
                )

    summary_lines = build_summary_from_existing_del_logs(root)
    summary_path = summary_file_path(root)
    with summary_path.open("w", encoding="utf-8", errors="strict") as f:
        for line in summary_lines:
            f.write(line)


def main() -> None:
    """
    功能：
        命令行入口：清理 R_candidates 下的大文件候选，并生成 del.log。

    参数：
        无

    返回：
        无
    """
    parser = argparse.ArgumentParser(
        description="遍历 root/libname/case/R_candidates/version，按阈值规则移动大文件到 del_candidates，并记录 del.log 与汇总日志。"
    )
    parser.add_argument("root_dir", type=str, help="根目录路径（下一级为若干 libname）")
    args = parser.parse_args()

    clean_large_candidates(args.root_dir)


if __name__ == "__main__":
    main()
