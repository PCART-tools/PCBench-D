def functionalize(func: Callable, *, remove: str = "mutations") -> Callable:
    warn_deprecated("functionalize")
    return _impl.functionalize(func, remove=remove)
