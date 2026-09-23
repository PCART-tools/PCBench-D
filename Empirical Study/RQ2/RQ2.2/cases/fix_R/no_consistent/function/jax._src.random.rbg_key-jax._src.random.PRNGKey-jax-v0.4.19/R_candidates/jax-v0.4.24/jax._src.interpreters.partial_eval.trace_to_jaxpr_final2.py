@profiler.annotate_function
def trace_to_jaxpr_final2(
    fun: lu.WrappedFun, debug_info: DebugInfo | None = None
  ) -> tuple[Jaxpr, OutputType, list[Any]]:
  with core.new_base_main(DynamicJaxprTrace) as main:  # type: ignore
    main.jaxpr_stack = ()  # type: ignore
    with core.new_sublevel():
      jaxpr, out_type, consts = trace_to_subjaxpr_dynamic2(fun, main, debug_info)
    del fun, main
  return jaxpr, out_type, consts
