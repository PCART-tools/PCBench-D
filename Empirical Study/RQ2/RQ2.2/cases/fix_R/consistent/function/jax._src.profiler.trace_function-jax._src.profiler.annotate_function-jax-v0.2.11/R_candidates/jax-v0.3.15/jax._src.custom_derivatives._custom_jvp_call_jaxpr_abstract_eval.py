def _custom_jvp_call_jaxpr_abstract_eval(*args, fun_jaxpr: core.ClosedJaxpr, **params):
  del args, params
  if fun_jaxpr.effects:
    raise NotImplementedError('Effects not supported in `custom_jvp`.')
  return fun_jaxpr.out_avals, fun_jaxpr.effects
