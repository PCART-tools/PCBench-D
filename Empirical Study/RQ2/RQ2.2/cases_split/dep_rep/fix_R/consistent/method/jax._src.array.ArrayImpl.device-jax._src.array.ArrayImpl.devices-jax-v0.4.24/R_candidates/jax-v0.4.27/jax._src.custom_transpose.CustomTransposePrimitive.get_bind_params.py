  def get_bind_params(self, params):
    assert 'call_jaxpr' in params
    assert 'transpose_jaxpr_thunk' in params
    new_params = dict(params)
    new_params['transpose'] = make_transpose_from_thunk(
        new_params.pop('transpose_jaxpr_thunk'),
        new_params['lin_tree'])
    call = lu.wrap_init(core.jaxpr_as_fun(new_params.pop('call_jaxpr')))
    return [call], new_params
