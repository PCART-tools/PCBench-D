def rearrange_binders(jaxpr: core.ClosedJaxpr, primals_in, tangents_in, primals_out, tangents_out):
  new_invars = _perm(primals_in, tangents_in, jaxpr.jaxpr.invars)
  new_outvars = _perm(primals_out, tangents_out, jaxpr.jaxpr.outvars)
  new_jaxpr = core.Jaxpr(jaxpr.jaxpr.constvars,
                         new_invars, new_outvars, jaxpr.jaxpr.eqns,
                         jaxpr.jaxpr.effects)
  return core.ClosedJaxpr(new_jaxpr, jaxpr.consts)
