@profiler.annotate_function
def trace_to_jaxpr_dynamic(
    fun: lu.WrappedFun,
    in_avals: Sequence[AbstractValue],
    debug_info: DebugInfo | None = None,
    *,
    keep_inputs: list[bool] | None = None,
) -> tuple[Jaxpr, list[AbstractValue], list[Any], list[tuple[Any, str]]]:
  with core.new_main(DynamicJaxprTrace, dynamic=True) as main:  # type: ignore
    main.jaxpr_stack = ()  # type: ignore
    jaxpr, out_avals, consts, attrs_tracked = trace_to_subjaxpr_dynamic(
      fun, main, in_avals, keep_inputs=keep_inputs, debug_info=debug_info)
    del main, fun
  return jaxpr, out_avals, consts, attrs_tracked
