def _dynamo_config_patch_proxy_dunder_call(
    self: Any, func: Callable[_P, _R]
) -> Callable[_P, _R]:
    @functools.wraps(func)
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        with self:
            return func(*args, **kwargs)

    return inner
