  def get_bind_params(self, params):
    new_params = dict(params)
    jaxpr = new_params.pop('call_jaxpr')
    subfun = lu.hashable_partial(lu.wrap_init(eval_jaxpr), jaxpr, ())
    axes = new_params.pop('out_axes')
    new_params['out_axes_thunk'] = HashableFunction(lambda: axes, closure=axes)
    return [subfun], new_params
