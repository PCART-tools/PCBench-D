def call_padding_rule(prim, in_avals, out_avals, *args, call_jaxpr, **params):
  if call_jaxpr.constvars: raise NotImplementedError
  padded_jaxpr, padded_consts = pad_jaxpr(call_jaxpr, ())
  if padded_consts: raise NotImplementedError
  new_params = dict(params, call_jaxpr=padded_jaxpr)
  subfuns, bind_params = prim.get_bind_params(new_params)
  return prim.bind(*subfuns, *args, **bind_params)
