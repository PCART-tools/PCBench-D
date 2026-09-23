def _custom_vjp_call_jaxpr_abstract_eval(*_, fun_jaxpr, **__):
  disallowed_effects = allowed_effects.filter_not_in(fun_jaxpr.effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `custom_vjp`: {disallowed_effects}')
  return fun_jaxpr.out_avals, fun_jaxpr.effects
