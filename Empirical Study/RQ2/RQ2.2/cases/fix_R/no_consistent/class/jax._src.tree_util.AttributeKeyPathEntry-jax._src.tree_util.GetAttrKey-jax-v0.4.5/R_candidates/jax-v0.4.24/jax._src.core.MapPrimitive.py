class MapPrimitive(Primitive):
  multiple_results = True
  map_primitive = True

  def bind(self, fun, *args, **params):
    assert len(params['in_axes']) == len(args)
    return map_bind(self, fun, *args, **params)

  def process(self, trace, fun, tracers, params):
    return trace.process_map(self, fun, tracers, params)

  def post_process(self, trace, out_tracers, params):
    return trace.post_process_map(self, out_tracers, params)

  def get_bind_params(self, params):
    new_params = dict(params)
    jaxpr = new_params.pop('call_jaxpr')
    subfun = lu.hashable_partial(lu.wrap_init(eval_jaxpr), jaxpr, ())
    axes = new_params.pop('out_axes')
    new_params['out_axes_thunk'] = HashableFunction(lambda: axes, closure=axes)
    return [subfun], new_params
