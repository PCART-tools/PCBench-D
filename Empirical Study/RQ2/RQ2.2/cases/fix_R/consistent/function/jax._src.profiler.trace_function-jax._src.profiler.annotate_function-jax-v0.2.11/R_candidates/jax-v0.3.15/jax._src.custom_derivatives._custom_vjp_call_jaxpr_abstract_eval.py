def _custom_vjp_call_jaxpr_abstract_eval(*_, fun_jaxpr, **__):
  if fun_jaxpr.effects:
    raise NotImplementedError('Effects not supported in `custom_vjp`.')
  return fun_jaxpr.out_avals, fun_jaxpr.effects
