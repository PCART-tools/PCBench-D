def trace_to_subjaxpr_dynamic(
    fun: lu.WrappedFun,
    main: core.MainTrace,
    in_avals: Sequence[AbstractValue],
    *,
    keep_inputs: Sequence[bool] | None = None,
    debug_info: DebugInfo | None = None,
) -> tuple[Jaxpr, list[AbstractValue], list[Any]]:
  keep_inputs = [True] * len(in_avals) if keep_inputs is None else keep_inputs

  frame = JaxprStackFrame()
  frame.debug_info = debug_info
  with extend_jaxpr_stack(main, frame), source_info_util.reset_name_stack():
    trace = DynamicJaxprTrace(main, core.cur_sublevel())
    in_tracers = _input_type_to_tracers(trace.new_arg, in_avals)
    in_tracers_ = [t for t, keep in zip(in_tracers, keep_inputs) if keep]
    ans = fun.call_wrapped(*in_tracers_)
    out_tracers = map(trace.full_raise, ans)
    jaxpr, consts = frame.to_jaxpr(out_tracers)
    del fun, main, trace, frame, in_tracers, out_tracers, ans
  config.jax_enable_checks and core.check_jaxpr(jaxpr)
  return jaxpr, [v.aval for v in jaxpr.outvars], consts
