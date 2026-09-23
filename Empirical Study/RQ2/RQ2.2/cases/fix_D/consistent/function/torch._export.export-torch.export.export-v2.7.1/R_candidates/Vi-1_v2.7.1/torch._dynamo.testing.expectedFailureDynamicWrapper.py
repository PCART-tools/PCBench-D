def expectedFailureDynamicWrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
    fn._expected_failure_dynamic_wrapper = True  # type: ignore[attr-defined]
    return fn
