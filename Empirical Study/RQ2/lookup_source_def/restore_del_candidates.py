import argparse
import shutil
from pathlib import Path
from typing import Iterable


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
        candidate = dst_dir / f"{src.stem}__restoredup{i}{src.suffix}"
        if not candidate.exists():
            return candidate

    raise RuntimeError(f"目标目录存在过多同名文件，无法生成唯一文件名: {dst_dir}/{file_name}")


def restore_del_candidates(root_dir: str | Path) -> None:
    """
    功能：
        遍历 root/libname/case/del_candidates/<version> 结构，
        将其中的 .py 文件移动回 case/R_candidates/<version>/ 下。

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
            del_root = case_dir / "del_candidates"
            if not del_root.is_dir():
                continue

            print(f"processing: {lib_dir.name}/{case_dir.name}")

            r_candidates_dir = case_dir / "R_candidates"
            r_candidates_dir.mkdir(parents=True, exist_ok=True)

            for version_dir in iter_subdirs(del_root):
                dst_version_dir = r_candidates_dir / version_dir.name
                dst_version_dir.mkdir(parents=True, exist_ok=True)

                for py_file in iter_py_files(version_dir):
                    dst = unique_destination_path(dst_version_dir, py_file.name)
                    py_file.rename(dst)

            try:
                shutil.rmtree(del_root)
            except OSError as exc:
                print(f"[WARN] 删除目录失败 {del_root}: {exc}")


def main() -> None:
    """
    功能：
        命令行入口：将 del_candidates 回滚到 R_candidates。

    参数：
        无

    返回：
        无
    """
    parser = argparse.ArgumentParser(
        description="遍历 root/libname/case/del_candidates/<version>，将 .py 移回 case/R_candidates/<version>/。"
    )
    parser.add_argument("root_dir", type=str, help="根目录路径（下一级为若干 libname）")
    args = parser.parse_args()

    restore_del_candidates(args.root_dir)


if __name__ == "__main__":
    main()
