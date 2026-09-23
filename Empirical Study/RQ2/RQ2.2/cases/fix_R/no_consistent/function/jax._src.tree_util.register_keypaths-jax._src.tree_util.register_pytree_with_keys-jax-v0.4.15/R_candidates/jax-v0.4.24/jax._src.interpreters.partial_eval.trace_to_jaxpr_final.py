@profiler.annotate_function
def trace_to_jaxpr_final(
    fun: lu.WrappedFun,
    in_avals: Sequence[AbstractValue],
    debug_info: DebugInfo | None = None,
    keep_inputs: Sequence[bool] | None = None,
) -> tuple[Jaxpr, list[AbstractValue], list[Any]]:
  with core.new_base_main(DynamicJaxprTrace) as main:  # type: ignore
    main.jaxpr_stack = ()  # type: ignore
    with core.new_sublevel():
      jaxpr, out_avals, consts, () = trace_to_subjaxpr_dynamic(
        fun, main, in_avals, keep_inputs=keep_inputs, debug_info=debug_info)
    del fun, main
  return jaxpr, out_avals, consts
