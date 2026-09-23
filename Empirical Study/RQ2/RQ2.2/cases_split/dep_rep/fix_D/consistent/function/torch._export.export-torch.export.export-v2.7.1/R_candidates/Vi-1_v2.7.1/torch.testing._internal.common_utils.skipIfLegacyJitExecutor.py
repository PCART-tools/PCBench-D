def skipIfLegacyJitExecutor(msg="test doesn't currently work with legacy JIT executor"):
    def decorator(fn):
        if not isinstance(fn, type):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                if GRAPH_EXECUTOR == ProfilingMode.LEGACY:
                    raise unittest.SkipTest(msg)
                else:
                    fn(*args, **kwargs)
            return wrapper

        assert isinstance(fn, type)
        if GRAPH_EXECUTOR == ProfilingMode.LEGACY:
            fn.__unittest_skip__ = True  # type: ignore[attr-defined]
            fn.__unittest_skip_why__ = msg  # type: ignore[attr-defined]

        return fn


    return decorator
