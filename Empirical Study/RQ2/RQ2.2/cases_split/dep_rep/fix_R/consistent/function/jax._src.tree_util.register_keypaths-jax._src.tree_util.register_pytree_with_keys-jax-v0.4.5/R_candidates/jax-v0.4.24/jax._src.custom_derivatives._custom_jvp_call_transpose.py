def _custom_jvp_call_transpose(params, jaxpr, args, ct, _, reduce_axes):
  del params
  return ad.backward_pass(jaxpr.jaxpr, reduce_axes, None, jaxpr.consts, args, ct)
