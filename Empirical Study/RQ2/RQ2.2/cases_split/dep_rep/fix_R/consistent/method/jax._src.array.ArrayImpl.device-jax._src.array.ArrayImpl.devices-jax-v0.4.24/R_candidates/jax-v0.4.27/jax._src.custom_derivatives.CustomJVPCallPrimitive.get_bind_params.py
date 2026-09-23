  def get_bind_params(self, params):
    new_params = dict(params)
    call_jaxpr = new_params.pop('call_jaxpr')
    num_consts = new_params.pop('num_consts')
    jvp_jaxpr_thunk = new_params.pop('jvp_jaxpr_thunk')
    fun = lu.wrap_init(core.jaxpr_as_fun(call_jaxpr))
    jvp = lift_jvp(num_consts, jvp_jaxpr_thunk)
    return [fun, jvp], new_params
