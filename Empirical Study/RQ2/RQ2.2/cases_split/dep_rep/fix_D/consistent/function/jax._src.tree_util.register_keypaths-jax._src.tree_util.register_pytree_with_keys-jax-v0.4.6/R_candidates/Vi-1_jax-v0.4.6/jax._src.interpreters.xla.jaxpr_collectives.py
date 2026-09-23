def jaxpr_collectives(jaxpr):
  """Generates all the collective primitives anywhere inside a Jaxpr."""
  for eqn in jaxpr.eqns:
    if eqn.primitive in _collective_primitives:
      yield eqn.primitive
  for subjaxpr in core.subjaxprs(jaxpr): yield from jaxpr_collectives(subjaxpr)
