def scan_bind(*args, **params):
  if config.enable_checks.value:
    avals = _map(core.get_aval, args)
    in_atoms = [core.Var(0, '', a) for a in avals]  # dummies
    _scan_typecheck(True, *in_atoms, **params)
    core.check_jaxpr(params['jaxpr'].jaxpr)
  return core.AxisPrimitive.bind(scan_p, *args, **params)
