def skipIfNotPy312(fn: Callable[..., Any]) -> Callable[..., Any]:
    if sys.version_info >= (3, 12):
        return fn
    return unittest.skip("Requires Python 3.12+")(fn)
