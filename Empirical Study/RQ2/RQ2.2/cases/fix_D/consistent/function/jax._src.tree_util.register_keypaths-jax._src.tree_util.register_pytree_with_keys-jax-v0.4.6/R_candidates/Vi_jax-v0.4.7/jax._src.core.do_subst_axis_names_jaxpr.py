def do_subst_axis_names_jaxpr(jaxpr: Union[Jaxpr, ClosedJaxpr], subst: AxisSubst):
  consts = None
  if isinstance(jaxpr, ClosedJaxpr):
    consts = jaxpr.consts
    jaxpr = jaxpr.jaxpr
  var_map: Dict[Var, Var] = {}
  invars = [subst_axis_names_var(v, subst, var_map) for v in jaxpr.invars]  # type: ignore[union-attr]
  constvars = [subst_axis_names_var(v, subst, var_map) for v in jaxpr.constvars]  # type: ignore[union-attr]
  eqns = [subst_axis_names_eqn(eqn, subst, var_map) for eqn in jaxpr.eqns]  # type: ignore[union-attr]
  outvars: List[Atom] = [v if isinstance(v, Literal) else var_map[v] for v in jaxpr.outvars]  # type: ignore[union-attr]
  new_jaxpr = Jaxpr(constvars, invars, outvars, eqns, jaxpr.effects)
  if consts is not None:
    return ClosedJaxpr(new_jaxpr, consts)
  return new_jaxpr
