def subst_axis_names_eqn(eqn: JaxprEqn, subst: AxisSubst, var_map: Dict[Var, Var]) -> JaxprEqn:
  invars: List[Atom] = [v if isinstance(v, Literal) else var_map[v] for v in eqn.invars]
  try:
    outvars = [subst_axis_names_var(v, subst, var_map) for v in eqn.outvars]
  except DuplicateAxisNameError as e:
    e.eqn = eqn
    raise
  params = subst_axis_names(eqn.primitive, eqn.params, subst)
  return eqn.replace(invars=invars, outvars=outvars, params=params)
