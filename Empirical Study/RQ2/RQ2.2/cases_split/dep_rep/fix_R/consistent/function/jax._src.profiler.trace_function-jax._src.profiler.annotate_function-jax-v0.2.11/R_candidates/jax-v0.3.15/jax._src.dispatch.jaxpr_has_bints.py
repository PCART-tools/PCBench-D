def jaxpr_has_bints(jaxpr: core.Jaxpr) -> bool:
  return (any(type(v.aval) is core.AbstractBInt for v in jaxpr.invars) or
          any(type(v.aval) is core.AbstractBInt
              for j in itertools.chain([jaxpr], core.subjaxprs(jaxpr))
              for e in j.eqns for v in e.outvars))
