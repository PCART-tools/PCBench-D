def count(fn: Callable[_P, _R]) -> Callable[_P, _R]:
    @functools.wraps(fn)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        if fn.__qualname__ not in simple_call_counter:
            simple_call_counter[fn.__qualname__] = 0
        simple_call_counter[fn.__qualname__] = simple_call_counter[fn.__qualname__] + 1
        return fn(*args, **kwargs)
    return wrapper
