def trace_to_subjaxpr_dynamic2(
    fun: lu.WrappedFun, main: core.MainTrace,
    debug_info: DebugInfo | None = None
) -> tuple[Jaxpr, OutputType, list[Any]]:
  in_avals, keep_inputs = unzip2(fun.in_type)
  frame = JaxprStackFrame()
  frame.debug_info = debug_info
  with extend_jaxpr_stack(main, frame), source_info_util.reset_name_stack():
    trace = DynamicJaxprTrace(main, core.cur_sublevel())
    in_tracers = _input_type_to_tracers(trace.new_arg, in_avals)
    in_tracers_ = [t for t, keep in zip(in_tracers, keep_inputs) if keep]
    ans = fun.call_wrapped(*in_tracers_)
    out_tracers = map(trace.full_raise, ans)
    jaxpr, out_type, consts = frame.to_jaxpr2(out_tracers)
    del fun, main, trace, frame, in_tracers, out_tracers, ans
  return jaxpr, out_type, consts
