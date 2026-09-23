def _has_refs(eqn: core.JaxprEqn):
  return any(isinstance(v.aval, AbstractRef) for v in eqn.invars)
