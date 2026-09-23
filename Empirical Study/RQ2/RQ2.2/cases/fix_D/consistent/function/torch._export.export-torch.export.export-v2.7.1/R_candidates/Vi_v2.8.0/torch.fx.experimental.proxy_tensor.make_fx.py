def make_fx(
    f: Callable,
    decomposition_table: Optional[Mapping[OpOverload, Callable]] = None,
    tracing_mode: str = "real",
    _allow_non_fake_inputs: bool = False,
    *,
    pre_dispatch: bool = False,
    record_module_stack: bool = False,
    _allow_fake_constant: bool = False,
    _error_on_data_dependent_ops: bool = True,
    stack_trace: bool = False,
) -> Callable[..., GraphModule]:
    """
    Given a function f, return a new function which when executed with valid
    arguments to f, returns an FX GraphModule representing the set of operations that
    were executed during the course of execution.

    If stack_trace is True, the stack_trace will be preserved on node.meta["stack_trace"]
    """

    assert tracing_mode in ["real", "fake", "symbolic"]

    from torch._inductor import config

    make_fx_tracer = _MakefxTracer(
        decomposition_table,
        tracing_mode,
        _allow_non_fake_inputs,
        pre_dispatch,
        record_module_stack,
        _allow_fake_constant,
        _error_on_data_dependent_ops,
        stack_trace=stack_trace or config.trace.enabled,
    )

    @functools.wraps(f)
    def wrapped(*args: object) -> GraphModule:
        return make_fx_tracer.trace(f, *args)

    return wrapped
