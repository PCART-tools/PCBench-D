def _eval_jaxpr_padded(
    jaxpr: Jaxpr, consts: list[Const], *args: DynamicJaxprTracer
  ) -> list[Const | DynamicJaxprTracer]:
  env: dict[Var, Val] = {}

  def read(x):
    return x.val if type(x) is Literal else env[x]

  def write(v, val) -> None:
    env[v] = val

  map(write, jaxpr.constvars, consts)
  map(write, jaxpr.invars, args)
  last_used = core.last_used(jaxpr)
  for eqn in jaxpr.eqns:
    in_avals  = [_substitute_axis_sizes(env, v.aval) for v in eqn.invars]
    out_avals = [_substitute_axis_sizes(env, v.aval) for v in eqn.outvars]
    rule = padding_rules[eqn.primitive]
    outs = rule(in_avals, out_avals, *map(read, eqn.invars), **eqn.params)
    map(write, eqn.outvars, outs)
    core.clean_up_dead_vars(eqn, env, last_used)
  return map(read, jaxpr.outvars)
