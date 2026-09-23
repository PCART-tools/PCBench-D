def xfailIfPy312(fn: Callable[..., Any]) -> Callable[..., Any]:
    if sys.version_info >= (3, 12):
        return unittest.expectedFailure(fn)
    return fn
