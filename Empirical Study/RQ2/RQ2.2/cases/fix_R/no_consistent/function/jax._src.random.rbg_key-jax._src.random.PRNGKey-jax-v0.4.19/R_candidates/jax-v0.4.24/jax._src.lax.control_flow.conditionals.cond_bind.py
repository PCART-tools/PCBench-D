def cond_bind(*args, branches, linear):
  if config.enable_checks.value:
    avals = map(core.get_aval, args)
    in_atoms = [core.Var(0, '', a) for a in avals]  # dummies
    _cond_typecheck(True, *in_atoms, branches=branches, linear=linear)
    for jaxpr in branches:
      core.check_jaxpr(jaxpr.jaxpr)
  return core.AxisPrimitive.bind(cond_p, *args, branches=branches, linear=linear)
