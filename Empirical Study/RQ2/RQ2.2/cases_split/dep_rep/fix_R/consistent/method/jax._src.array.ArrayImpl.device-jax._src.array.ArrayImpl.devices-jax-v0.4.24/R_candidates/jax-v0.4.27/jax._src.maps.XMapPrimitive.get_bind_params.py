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
