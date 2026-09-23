def jaxpr_literals(jaxpr):
  """Generates all the literals inside a jaxpr, including nested subjaxprs."""
  for eqn in jaxpr.eqns:
    for v in eqn.invars:
      if type(v) is core.Literal:
        yield v.val
  for subjaxpr in core.subjaxprs(jaxpr):
    yield from jaxpr_literals(subjaxpr)
