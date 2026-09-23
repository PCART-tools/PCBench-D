def expectedFailureDynamic(fn: Callable[..., Any]) -> Callable[..., Any]:
    fn._expected_failure_dynamic = True  # type: ignore[attr-defined]
    return fn
