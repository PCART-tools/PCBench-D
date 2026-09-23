class XMapPrimitive(core.MapPrimitive):
  def __init__(self):
    super().__init__('xmap')
    self.def_impl(xmap_impl)
    self.def_custom_bind(self.bind)

  def bind(self, fun, *args, in_axes, **params):
    assert len(in_axes) == len(args), (in_axes, args)
    return core.map_bind(self, fun, *args, in_axes=in_axes, **params)

  def process(self, trace, fun, tracers, params):
    return trace.process_xmap(self, fun, tracers, params)

  def post_process(self, trace, out_tracers, params):
    post_process = getattr(trace, 'post_process_xmap', None)
    if post_process is None:
      raise NotImplementedError
    return post_process(self, out_tracers, params)

  def get_bind_params(self, params):
    new_params = dict(params)
    jaxpr = new_params.pop('call_jaxpr')
    subfun = lu.hashable_partial(lu.wrap_init(core.eval_jaxpr), jaxpr, ())
    axes = new_params.pop('out_axes')
    new_params['out_axes_thunk'] = HashableFunction(lambda: axes, closure=axes)
    spmd_axes = new_params.pop('spmd_out_axes')
    if spmd_axes is not None:
      new_params['spmd_out_axes_thunk'] = \
          HashableFunction(lambda: spmd_axes, closure=spmd_axes)
    else:
      new_params['spmd_out_axes_thunk'] = None
    return [subfun], new_params
