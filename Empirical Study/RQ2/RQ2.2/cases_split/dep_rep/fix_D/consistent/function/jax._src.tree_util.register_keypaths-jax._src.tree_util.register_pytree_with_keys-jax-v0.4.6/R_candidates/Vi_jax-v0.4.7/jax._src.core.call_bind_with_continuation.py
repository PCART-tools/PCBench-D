def call_bind_with_continuation(primitive: CallPrimitive, fun, *args, **params):
  top_trace = find_top_trace(args)
  fun_, env_trace_todo = process_env_traces_call(
      fun, primitive, top_trace.level, tuple(params.items()))
  tracers = map(top_trace.full_raise, args)
  fun_ = lu.annotate(fun_, fun.in_type)

  def call_bind_continuation(outs):
    return map(full_lower, apply_todos(env_trace_todo(), outs))
  return call_bind_continuation, top_trace, fun_, tracers, params
