def new_jaxpr_eqn(invars, outvars, primitive, params, effects, source_info=None):
  source_info = source_info or source_info_util.new_source_info()
  if config.jax_enable_checks:
    assert all(isinstance(x, (Var, Literal)) for x in  invars)
    assert all(isinstance(v,  Var)           for v in outvars)
  return JaxprEqn(invars, outvars, primitive, params, effects, source_info)
