def requiresPy310(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    if sys.version_info >= (3, 10):
        return fn
    else:
        return unittest.skip("Requires Python 3.10+")(fn)
