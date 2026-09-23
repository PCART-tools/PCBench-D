@weakref_lru_cache
def convert_invars_to_constvars(jaxpr: Jaxpr, n: int) -> Jaxpr:
  """Move n invars to constvars. Like an inverse of convert_constvars_Jaxpr."""
  if any(isinstance(eff, effects.JaxprInputEffect) for eff in jaxpr.effects):
    raise NotImplementedError
  config.jax_enable_checks and core.check_jaxpr(jaxpr)
  constvars, invars = split_list(jaxpr.invars, [n])
  dbg = jaxpr.debug_info and jaxpr.debug_info._replace(
      arg_names=jaxpr.debug_info.arg_names[n:])
  lifted_jaxpr = jaxpr.replace(constvars=tuple(constvars), invars=invars,
                               debug_info=dbg)
  config.jax_enable_checks and core.check_jaxpr(lifted_jaxpr)
  return lifted_jaxpr
