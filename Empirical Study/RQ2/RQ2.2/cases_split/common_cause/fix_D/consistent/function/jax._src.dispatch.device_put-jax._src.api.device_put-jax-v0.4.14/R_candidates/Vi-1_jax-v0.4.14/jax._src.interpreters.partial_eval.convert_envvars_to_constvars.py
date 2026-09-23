def convert_envvars_to_constvars(jaxpr: Jaxpr, num_env_vars: int) -> Jaxpr:
  if any(isinstance(eff, effects.JaxprInputEffect) for eff in jaxpr.effects):
    raise NotImplementedError
  config.jax_enable_checks and core.check_jaxpr(jaxpr)
  env_vars, invars = split_list(jaxpr.invars, [num_env_vars])
  converted_jaxpr = Jaxpr(constvars=jaxpr.constvars + env_vars,
                          invars=invars, outvars=jaxpr.outvars, eqns=jaxpr.eqns,
                          effects=jaxpr.effects)
  config.jax_enable_checks and core.check_jaxpr(converted_jaxpr)
  return converted_jaxpr
