class CustomJVPCallPrimitive(core.Primitive):
  multiple_results = True

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

  def impl(self, fun, _, *args):
    with core.new_sublevel():
      return fun.call_wrapped(*args)

  def post_process(self, trace, out_tracers, jvp_was_run: bool):
    return trace.post_process_custom_jvp_call(out_tracers, jvp_was_run)

  def get_bind_params(self, params):
    new_params = dict(params)
    call_jaxpr = new_params.pop('call_jaxpr')
    num_consts = new_params.pop('num_consts')
    jvp_jaxpr_thunk = new_params.pop('jvp_jaxpr_thunk')
    fun = lu.wrap_init(core.jaxpr_as_fun(call_jaxpr))
    jvp = lift_jvp(num_consts, jvp_jaxpr_thunk)
    return [fun, jvp], new_params
