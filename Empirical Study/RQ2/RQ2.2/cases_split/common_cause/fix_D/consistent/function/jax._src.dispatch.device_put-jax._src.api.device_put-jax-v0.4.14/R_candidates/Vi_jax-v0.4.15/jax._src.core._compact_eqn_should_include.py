def _compact_eqn_should_include(k: str, v: Any) -> bool:
  if k == 'branches': return False
  if isinstance(v, (Jaxpr, ClosedJaxpr)): return False
  if (isinstance(v, tuple) and
      any(isinstance(e, (Jaxpr, ClosedJaxpr)) for e in v)):
    return False
  return True
