def skipIfPy312(fn: Callable[..., Any]) -> Callable[..., Any]:
    if sys.version_info >= (3, 12):
        return unittest.skip("Not supported in Python 3.12+")(fn)
    return fn
