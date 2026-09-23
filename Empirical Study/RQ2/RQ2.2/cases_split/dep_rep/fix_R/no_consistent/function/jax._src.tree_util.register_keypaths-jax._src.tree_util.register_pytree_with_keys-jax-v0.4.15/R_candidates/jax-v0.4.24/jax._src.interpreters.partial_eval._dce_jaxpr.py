@weakref_lru_cache
def _dce_jaxpr(jaxpr: Jaxpr, used_outputs: tuple[bool, ...],
               instantiate: tuple[bool, ...]
               ) -> tuple[Jaxpr, list[bool]]:
  env: dict[Var, bool] = {}

  def read(v: Var) -> bool:
    return env.get(v, False)

  def write(x: Atom, b: bool) -> None:
    if type(x) is Var:
      env[x] = read(x) or b

  def has_effects(e: JaxprEqn) -> bool:
    return bool(e.effects) or core.primitive_uses_outfeed(e.primitive, e.params)

  new_eqns = []
  map(write, jaxpr.outvars, used_outputs)
  for eqn in jaxpr.eqns[::-1]:
    used_outs = map(read, eqn.outvars)
    if not any(used_outs) and not has_effects(eqn):
      used_ins = [False] * len(eqn.invars)
    else:
      rule = dce_rules.get(eqn.primitive, _default_dce_rule)
      used_ins, new_eqn = rule(used_outs, eqn)
      if new_eqn is not None:
        new_eqns.append(new_eqn)
    map(write, eqn.invars, used_ins)
  used_inputs = map(read, jaxpr.invars)
  used_inputs = map(op.or_, instantiate, used_inputs)

  invars = [v for v, b in zip(jaxpr.invars, used_inputs)   if b]
  outvars = [v for v, b in zip(jaxpr.outvars, used_outputs) if b]
  eqns = new_eqns[::-1]
  jaxpr_effects = make_jaxpr_effects(jaxpr.constvars, invars, outvars, eqns)

  dbg = jaxpr.debug_info and core.JaxprDebugInfo(
      jaxpr.debug_info.traced_for, jaxpr.debug_info.func_src_info,
      tuple(v for v, b in zip(jaxpr.debug_info.arg_names, used_inputs) if b),
      tuple(v for v, b in zip(jaxpr.debug_info.result_paths, used_outputs) if b))
  new_jaxpr = Jaxpr(jaxpr.constvars, invars, outvars, eqns, jaxpr_effects, dbg)
  config.enable_checks.value and core.check_jaxpr(new_jaxpr)

  return new_jaxpr, used_inputs
