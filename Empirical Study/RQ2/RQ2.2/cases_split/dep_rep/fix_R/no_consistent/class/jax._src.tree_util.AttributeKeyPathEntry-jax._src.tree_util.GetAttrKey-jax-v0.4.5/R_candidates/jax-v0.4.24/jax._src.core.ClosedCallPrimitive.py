class ClosedCallPrimitive(CallPrimitive):
  def get_bind_params(self, params):
    new_params = dict(params)
    jaxpr = new_params.pop('call_jaxpr')
    subfun = lu.wrap_init(partial(eval_jaxpr, jaxpr.jaxpr, jaxpr.consts))
    return [subfun], new_params
