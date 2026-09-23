@functools.lru_cache
def _function_source_info(fn: Callable) -> tuple[Sequence[str], int, str | None]:
    """Returns the source lines, line number, and source file path for the given function.

    Essentially, inspect.getsourcelines() and inspect.getsourcefile() combined.
    Caching is applied to reduce the performance impact of this function.
    """
    source_lines, lineno = inspect.getsourcelines(fn)
    return source_lines, lineno, inspect.getsourcefile(fn)
