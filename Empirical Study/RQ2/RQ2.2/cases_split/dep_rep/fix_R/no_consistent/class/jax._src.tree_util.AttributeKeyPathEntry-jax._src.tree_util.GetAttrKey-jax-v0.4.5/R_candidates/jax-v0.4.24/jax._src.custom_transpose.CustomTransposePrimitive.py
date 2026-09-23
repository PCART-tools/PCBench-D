class CustomTransposePrimitive(core.Primitive):
  call_primitive = False
  map_primitive = False
  multiple_results = True

  def bind(self, call, *args, **params):
    # TODO(frostig,mattjj): This doesn't handle closures yet, which is
    # a bit involved. Closures are complicated by us binding `call`
    # twice in the JVP rule for custom transpose. The `env_trace_todo`
    # output by `process_env_traces` due to one of those two bindings
    # should be passable to the other, and need to be passed onward
    # since the second bind is deferred by partial eval (since it
    # typically receives unknowns)
    top_trace = core.find_top_trace(args)
    tracers = map(top_trace.full_raise, args)
    outs = top_trace.process_custom_transpose(self, call, tracers, **params)
    return outs

  # TODO(frostig,mattjj): consider keeping `call` as a named parameter
  # instead of following this "call primitive" convention.
  def get_bind_params(self, params):
    assert 'call_jaxpr' in params
    assert 'transpose_jaxpr_thunk' in params
    new_params = dict(params)
    new_params['transpose'] = make_transpose_from_thunk(
        new_params.pop('transpose_jaxpr_thunk'),
        new_params['lin_tree'])
    call = lu.wrap_init(core.jaxpr_as_fun(new_params.pop('call_jaxpr')))
    return [call], new_params
