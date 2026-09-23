class CustomVJPCallPrimitive(core.CallPrimitive):
  initial_style: core.Primitive

  def bind(self, fun, fwd, bwd, *args, out_trees):
    args = map(core.full_lower, args)
    top_trace = core.find_top_trace(args)
    fun, env_trace_todo1 = process_env_traces(
        fun, self, top_trace and top_trace.level, False)
    fwd, env_trace_todo2 = process_env_traces_fwd(
      fwd, top_trace and top_trace.level, out_trees)
    tracers = map(top_trace.full_raise, args)  # type: ignore
    bwd_ = lu.wrap_init(lambda *args: bwd.call_wrapped(*args))
    outs = top_trace.process_custom_vjp_call(self, fun, fwd, bwd_, tracers,
                                             out_trees=out_trees)
    fst, env_trace_todo = lu.merge_linear_aux(env_trace_todo1, env_trace_todo2)
    if fst:
      return _apply_todos(env_trace_todo, map(core.full_lower, outs))
    else:
      env_trace_todo, bwd_transform = env_trace_todo
      bwd = _apply_bwd_transform(bwd_transform, bwd)
      return _apply_todos(env_trace_todo, map(core.full_lower, outs))

  def impl(self, fun, fwd, bwd, *args, out_trees):
    del fwd, bwd, out_trees
    with core.new_sublevel():
      return fun.call_wrapped(*args)

  def post_process(self, trace, out_tracers, params):
    return trace.post_process_custom_vjp_call(out_tracers, params)
