@weakref_lru_cache
def convert_constvars_jaxpr(jaxpr: Jaxpr) -> Jaxpr:
  """Moves the constvars to the start of invars."""
  config.jax_enable_checks and core.check_jaxpr(jaxpr)
  dbg = jaxpr.debug_info and jaxpr.debug_info._replace(
      arg_names=(None,) * len(jaxpr.constvars) + jaxpr.debug_info.arg_names)
  lifted_jaxpr = Jaxpr(constvars=(),
                       invars=jaxpr.constvars + jaxpr.invars,
                       outvars=jaxpr.outvars, eqns=jaxpr.eqns,
                       effects=jaxpr.effects, debug_info=dbg)
  config.jax_enable_checks and core.check_jaxpr(lifted_jaxpr)
  return lifted_jaxpr
