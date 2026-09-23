import warnings

def convert_py2_to_py3(source_code: str) -> str:
    """
    功能：
        将 Python 2 源码在内存中转换为 Python 3 源码。
        作为 ast.parse 无法解析历史版本代码时的兜底策略。

    参数：
        source_code: 原始的可能包含 Python 2 语法的源码字符串

    返回：
        转换后的合法 Python 3 源码字符串

    兼容性说明：
        - Python <= 3.12: 优先使用标准库 lib2to3
        - Python >= 3.13: 标准库移除 lib2to3，需安装 fissix 作为替代
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)

        try:
            import lib2to3.refactor as refactor
            fixes_pkg = "lib2to3.fixes"
        except ModuleNotFoundError:
            try:
                import fissix.refactor as refactor
                fixes_pkg = "fissix.fixes"
            except ModuleNotFoundError as exc:
                raise ModuleNotFoundError(
                    "未找到 lib2to3（Python 3.13+ 已移除该标准库模块）。"
                    "请在当前环境安装 fissix（pip install fissix / conda install -c conda-forge fissix），"
                    "或使用 Python<=3.12 运行。"
                ) from exc

        fixers = refactor.get_fixers_from_package(fixes_pkg)
        tool = refactor.RefactoringTool(fixers)
        tree = tool.refactor_string(source_code + "\n", "fallback_py2_to_py3")
        return str(tree)
