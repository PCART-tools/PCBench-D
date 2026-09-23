  def bind(self, fun, jvp, *args, symbolic_zeros):
    args = map(core.full_lower, args)
    top_trace = core.find_top_trace(args)
    fun, env_trace_todo1 = process_env_traces(
        fun, self, top_trace and top_trace.level, False)
    jvp, env_trace_todo2 = process_env_traces(
        jvp, self, top_trace and top_trace.level, True)
    tracers = map(top_trace.full_raise, args)  # type: ignore
    outs = top_trace.process_custom_jvp_call(self, fun, jvp, tracers,  # type: ignore
                                             symbolic_zeros=symbolic_zeros)  # type: ignore
    _, env_trace_todo = lu.merge_linear_aux(env_trace_todo1, env_trace_todo2)
    return core.apply_todos(env_trace_todo, map(core.full_lower, outs))
