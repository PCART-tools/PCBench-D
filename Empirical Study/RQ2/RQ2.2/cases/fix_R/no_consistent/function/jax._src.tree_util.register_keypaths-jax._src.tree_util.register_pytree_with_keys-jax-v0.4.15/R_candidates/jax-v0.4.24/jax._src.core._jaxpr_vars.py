def _jaxpr_vars(jaxpr) -> Iterable[Var]:
  return it.chain(
      jaxpr.invars, jaxpr.constvars,
      (v for eqn in jaxpr.eqns for v in eqn.outvars))
