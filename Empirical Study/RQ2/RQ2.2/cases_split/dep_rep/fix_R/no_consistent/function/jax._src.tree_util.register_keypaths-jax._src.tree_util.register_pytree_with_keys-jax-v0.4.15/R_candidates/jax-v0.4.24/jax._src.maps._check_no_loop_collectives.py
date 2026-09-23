def _check_no_loop_collectives(jaxpr, loop_axis_resources):
  if isinstance(jaxpr, core.ClosedJaxpr):
    jaxpr = jaxpr.jaxpr
  def subst_no_loop(name):
    if loop_axis_resources.get(name, ()):
      raise RuntimeError(f"Named axes with loop resources assigned to them cannot "
                          f"be referenced inside the xmapped computation (e.g. in "
                          f"collectives), but `{name}` violates that rule")
    return (name,)
  for eqn in jaxpr.eqns:
    core.subst_axis_names(eqn.primitive, eqn.params, subst_no_loop, traverse=False)
    rec = partial(_check_no_loop_collectives, loop_axis_resources=loop_axis_resources)
    core.traverse_jaxpr_params(rec, eqn.params)
