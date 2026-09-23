@profiler.annotate_function
def trace_to_jaxpr_dynamic2(
    fun: lu.WrappedFun, debug_info: DebugInfo | None = None
  ) -> tuple[Jaxpr, OutputType, list[Any]]:
  with core.new_main(DynamicJaxprTrace, dynamic=True) as main:  # type: ignore
    main.jaxpr_stack = ()  # type: ignore
    jaxpr, out_type, consts = trace_to_subjaxpr_dynamic2(fun, main, debug_info)
    del main, fun
  return jaxpr, out_type, consts
