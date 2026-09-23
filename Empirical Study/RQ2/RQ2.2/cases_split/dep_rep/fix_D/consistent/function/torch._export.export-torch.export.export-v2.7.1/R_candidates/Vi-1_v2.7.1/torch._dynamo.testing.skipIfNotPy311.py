def skipIfNotPy311(fn: Callable[..., Any]) -> Callable[..., Any]:
    if sys.version_info >= (3, 11):
        return fn
    return unittest.skip(fn)
