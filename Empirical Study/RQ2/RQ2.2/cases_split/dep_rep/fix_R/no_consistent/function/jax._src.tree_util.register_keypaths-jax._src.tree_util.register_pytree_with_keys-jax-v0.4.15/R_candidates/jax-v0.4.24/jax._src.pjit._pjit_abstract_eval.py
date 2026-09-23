def _pjit_abstract_eval(*args, jaxpr, out_shardings, resource_env, **_):
  return jaxpr.out_avals, jaxpr.effects
