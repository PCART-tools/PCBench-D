def skipIfNotPy311(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    if sys.version_info >= (3, 11):
        return fn
    return unittest.skip(fn)
