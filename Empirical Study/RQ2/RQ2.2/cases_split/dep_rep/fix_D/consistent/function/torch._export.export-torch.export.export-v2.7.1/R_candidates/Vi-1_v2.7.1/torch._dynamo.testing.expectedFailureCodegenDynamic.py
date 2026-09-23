def expectedFailureCodegenDynamic(fn: Callable[..., Any]) -> Callable[..., Any]:
    fn._expected_failure_codegen_dynamic = True  # type: ignore[attr-defined]
    return fn
