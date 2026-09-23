import ast
import os
import subprocess
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple


EXCLUDED_DIR_NAMES = {
    ".git",
    "__pycache__",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "env",
    "build",
    "dist",
    ".mypy_cache",
    ".pytest_cache",
}

# 适配不同目录结构的仓库：以下前缀表示源码根目录下多出的一层非包名目录。
# 例如 py-polars/polars/...、lib/matplotlib/...、src/transformers/...，
# 这些仓库按相对路径算出的 FQN 会多出一个前导分段，需去掉第一个分段。
_FQN_REDUNDANT_PREFIXES = {
    ("py-polars", "polars"),
    ("lib", "matplotlib"),
    ("lib", "mpl_toolkits"),
    ("src", "transformers"),
    ("src", "PIL"),
    ("python-package", "lightgbm"),
    ("python-package", "xgboost"),
    ("src", "click"),
    ("src", "flask"),
}


def run_cmd(cmd: Sequence[str], cwd: Optional[Path] = None) -> str:
    """
    功能：
        执行外部命令，并返回标准输出。

    参数：
        cmd : Sequence[str]
            命令及参数列表。
        cwd : Optional[Path]
            执行目录。

    返回：
        str
        标准输出内容。
    """
    result = subprocess.run(
        list(cmd),
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_repo_head(repo_root: Path) -> str:
    """
    功能：
        获取仓库当前 HEAD 的 commit hash。
    """
    return run_cmd(["git", "rev-parse", "HEAD"], cwd=repo_root)


def git_checkout_tag(repo_root: Path, version: str) -> None:
    """
    功能：
        将仓库切换到 tags/<version>。
    """
    run_cmd(["git", "checkout", "-f", f"tags/{version}"], cwd=repo_root)


def git_restore(repo_root: Path, commit_hash: str) -> None:
    """
    功能：
        将仓库恢复到指定 commit。
    """
    run_cmd(["git", "checkout", "-f", commit_hash], cwd=repo_root)


def should_skip_path(path: Path) -> bool:
    """
    功能：
        判断路径是否应跳过。
    """
    return any(part in EXCLUDED_DIR_NAMES for part in path.parts)


def iter_python_files(root: Path) -> Iterable[Path]:
    """
    功能：
        递归遍历 root 下全部 .py 文件，自动跳过排除目录。
    """
    for py_file in root.rglob("*.py"):
        if should_skip_path(py_file):
            continue
        if py_file.is_file():
            yield py_file


def read_text_best_effort(py_file: Path) -> Optional[str]:
    """
    功能：
        尝试用多种编码读取 Python 文件。
    """
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return py_file.read_text(encoding=enc)
        except Exception:
            continue
    return None


class ApiCollector(ast.NodeVisitor):
    """
    功能：
        基于 AST 提取指定粒度的 API 源码。

    type 定义：
        1 = 函数
        2 = 类
        3 = 方法
    """

    def __init__(self, api_type: int, source_text: str) -> None:
        self.api_type = api_type
        self.source_text = source_text
        self.lines = source_text.splitlines(keepends=True)
        self.class_stack: List[str] = []
        self.function_depth = 0
        self.results: List[Tuple[List[str], str]] = []

    def _get_node_source(self, node: ast.AST) -> str:
        """
        功能：
            提取节点源码，若有装饰器则一并包含。
        """
        start_lineno = getattr(node, "lineno", None)
        end_lineno = getattr(node, "end_lineno", None)

        decorators = getattr(node, "decorator_list", None) or []
        if decorators:
            decorator_start = min(getattr(d, "lineno", start_lineno) for d in decorators)
            if start_lineno is None or decorator_start < start_lineno:
                start_lineno = decorator_start

        if start_lineno is not None and end_lineno is not None:
            return "".join(self.lines[start_lineno - 1:end_lineno])

        segment = ast.get_source_segment(self.source_text, node)
        return segment or ""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._handle_function_like(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._handle_function_like(node)

    def _handle_function_like(self, node: ast.AST) -> None:
        """
        功能：
            统一处理普通函数和异步函数。
        """
        is_top_level_function = (not self.class_stack) and self.function_depth == 0
        is_direct_method = bool(self.class_stack) and self.function_depth == 0

        if self.api_type == 1 and is_top_level_function:
            self.results.append(([getattr(node, "name")], self._get_node_source(node)))
        elif self.api_type == 3 and is_direct_method:
            self.results.append(
                (self.class_stack + [getattr(node, "name")], self._get_node_source(node))
            )

        self.function_depth += 1
        try:
            self.generic_visit(node)
        finally:
            self.function_depth -= 1

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        功能：
            处理类定义。
        """
        if self.api_type == 2:
            self.results.append((self.class_stack + [node.name], self._get_node_source(node)))

        self.class_stack.append(node.name)
        try:
            self.generic_visit(node)
        finally:
            self.class_stack.pop()


def module_parts_from_file(repo_root: Path, py_file: Path) -> List[str]:
    """
    功能：
        计算 py_file 相对于 repo_root 的模块路径分段。

    例如：
        repo_root = /root/jax
        py_file   = /root/jax/jax/_src/random.py

        返回：
        ["jax", "_src", "random"]

        若文件为 __init__.py，则去掉最后的 "__init__"。
    """
    rel = py_file.relative_to(repo_root)
    parts = list(rel.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return parts


def normalize_module_parts(parts: List[str]) -> List[str]:
    """
    功能：
        适配不同目录结构的仓库：若模块前两段命中已知的多余前导目录，
        去掉第一个分段，使 FQN 回归真实的包结构。

    例如：
        ["py-polars", "polars", "dataframe"] -> ["polars", "dataframe"]
        ["lib", "matplotlib", "pyplot"]      -> ["matplotlib", "pyplot"]

    参数：
        parts : List[str]
            由 module_parts_from_file 得到的模块路径分段。

    返回：
        List[str]
            去掉多余前导分段后的模块路径分段。
    """
    if len(parts) >= 2 and (parts[0], parts[1]) in _FQN_REDUNDANT_PREFIXES:
        return parts[1:]
    return parts


def write_api_file(output_root: Path, fqn_parts: List[str], source_code: str) -> Path:
    """
    功能：
        将单个 API 源码写入 output_root，文件名为 完全限定名称.py。
    """
    output_root.mkdir(parents=True, exist_ok=True)
    fqn = ".".join([p for p in fqn_parts if p])
    out_file = output_root / f"{fqn}.py"
    out_file.write_text(
        source_code if source_code.endswith("\n") else source_code + "\n",
        encoding="utf-8",
    )
    return out_file


def extract_candidates(
    root: str | Path,
    libname: str,
    version: str,
    path: str,
    type: int,
    outputRoot: str | Path,
) -> List[Path]:
    """
    功能：
        提取指定仓库、指定 tag 版本、指定 path 下的所有 candidates。

    参数：
        root : str | Path
            仓库根目录，实际仓库路径为 root/libname。
        libname : str
            仓库目录名。
        version : str
            目标 tag 版本号，会执行 git checkout tags/<version>。
        path : str
            相对于 root/libname 的扫描子路径，也就是你说的 prefix。
            例如：
            - "" 或 "." 表示扫描整个仓库
            - "jax/_src" 表示只扫描该子目录
        type : int
            提取粒度：
            - 1 = 函数
            - 2 = 类
            - 3 = 方法
        outputRoot : str | Path
            输出目录。所有提取出的 API 都会以 “完全限定名称.py” 的形式写入该目录。

    返回：
        List[Path]
        所有成功写出的 API 文件路径列表。

    执行流程：
        1. cd 到 root/libname
        2. git checkout tags/version
        3. cd 到当前目录的 path
        4. 递归提取所有指定粒度 API
        5. 按从 root/libname 下一级开始的完全限定名称.py 存储到 outputRoot
        6. 最后恢复仓库到原始 commit
    """
    if type not in (1, 2, 3):
        raise ValueError("type 只能是 1=函数, 2=类, 3=方法")

    root = Path(root).expanduser().resolve()
    repo_root = (root / libname).resolve()
    output_root = Path(outputRoot).expanduser().resolve()

    if not repo_root.exists():
        raise FileNotFoundError(f"仓库不存在: {repo_root}")

    scan_root = (repo_root / path).resolve() if path and path != "." else repo_root

    try:
        scan_root.relative_to(repo_root)
    except ValueError:
        raise ValueError(f"path 必须位于 root/libname 内部: {path}")

    old_cwd = Path.cwd()
    original_head = get_repo_head(repo_root)
    written_files: List[Path] = []

    try:
        # 1. cd 到 root/libname
        os.chdir(repo_root)

        # 2. checkout 指定 tag
        git_checkout_tag(repo_root, version)

        if not scan_root.exists():
            raise FileNotFoundError(f"path 不存在: {scan_root}")

        # 3. cd 到 path
        os.chdir(scan_root)

        # 4. 递归提取 API
        for py_file in iter_python_files(scan_root):
            source_text = read_text_best_effort(py_file)
            if source_text is None:
                continue

            try:
                tree = ast.parse(source_text)
            except SyntaxError:
                continue

            collector = ApiCollector(api_type=type, source_text=source_text)
            collector.visit(tree)

            if not collector.results:
                continue

            # 注意：这里仍然相对 repo_root 计算 FQN
            # 这样输出名就是从 root/libname 下一级开始
            module_parts = module_parts_from_file(repo_root, py_file)
            module_parts = normalize_module_parts(module_parts)

            for api_name_parts, source_code in collector.results:
                fqn_parts = module_parts + api_name_parts
                out_file = write_api_file(output_root, fqn_parts, source_code)
                written_files.append(out_file)

    finally:
        os.chdir(old_cwd)
        git_restore(repo_root, original_head)

    return written_files