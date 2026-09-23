def cache(function: Callable[..., T]) -> T:  # noqa: D103
    # need this to satisfy mypy issue with "@property/@cache combination"
    # See: https://github.com/python/mypy/issues/5858
    return functools.lru_cache()(function)  # type: ignore[return-value]
