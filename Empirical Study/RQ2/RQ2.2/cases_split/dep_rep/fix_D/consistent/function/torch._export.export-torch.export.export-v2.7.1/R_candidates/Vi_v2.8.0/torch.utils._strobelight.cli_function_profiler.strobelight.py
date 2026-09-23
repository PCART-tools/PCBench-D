def strobelight(
    profiler: Optional[StrobelightCLIFunctionProfiler] = None, **kwargs: Any
) -> Callable[[Callable[_P, _R]], Callable[_P, Optional[_R]]]:
    if not profiler:
        profiler = StrobelightCLIFunctionProfiler(**kwargs)

    def strobelight_inner(
        work_function: Callable[_P, _R]
    ) -> Callable[_P, Optional[_R]]:
        @functools.wraps(work_function)
        def wrapper_function(*args: _P.args, **kwargs: _P.kwargs) -> Optional[_R]:
            return profiler.profile(work_function, *args, **kwargs)

        return wrapper_function

    return strobelight_inner
