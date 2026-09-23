def call_expr(func: SeriesMethod) -> SeriesMethod:
    """Dispatch Series method to an expression implementation."""

    @wraps(func)  # type: ignore[arg-type]
    def wrapper(self: Any, *args: P.args, **kwargs: P.kwargs) -> Series:
        s = wrap_s(self._s)
        expr = F.col(s.name)
        namespace = getattr(self, "_accessor", None)
        if namespace is not None:
            expr = getattr(expr, namespace)
        f = getattr(expr, func.__name__)
        return s.to_frame().select(f(*args, **kwargs)).to_series()

    # note: applying explicit '__signature__' helps IDEs (especially PyCharm)
    # with proper autocomplete, in addition to what @functools.wraps does
    setattr(wrapper, "__signature__", inspect.signature(func))  # noqa: B010
    return wrapper
