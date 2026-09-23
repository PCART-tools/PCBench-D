def init_once_fakemode(fn: Callable[..., Any]) -> Callable[[], Any]:
    """Wrapper around lazy init functions in fx_passes/"""

    @functools.lru_cache(None)
    @functools.wraps(fn)
    def lazy_init() -> Any:
        counters_ref = counters["inductor"].copy()

        with torch._guards.tracing(None), unset_fake_temporarily(), FakeTensorMode():
            result = fn()

        # clear view matches encountered during tracing
        counters["inductor"] = counters_ref

        return result

    return lazy_init
