def all_eqns(jaxpr: core.Jaxpr):
  for eqn in jaxpr.eqns:
    yield (jaxpr, eqn)
  for subjaxpr in core.subjaxprs(jaxpr):
    yield from all_eqns(subjaxpr)
