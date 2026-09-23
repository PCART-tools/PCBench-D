def get_nonrecursive_disable_wrapper(fn: Callable[_P, _R]) -> Callable[_P, _R]:
    # wrap function to get the right error message
    # this function is in external_utils so that convert_frame doesn't skip it.
    @functools.wraps(fn)
    def nonrecursive_disable_wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        return fn(*args, **kwargs)

    return nonrecursive_disable_wrapper
