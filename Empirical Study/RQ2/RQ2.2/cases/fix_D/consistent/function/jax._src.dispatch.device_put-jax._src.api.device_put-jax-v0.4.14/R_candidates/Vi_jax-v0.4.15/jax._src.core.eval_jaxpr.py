def eval_jaxpr(jaxpr: Jaxpr, consts, *args, propagate_source_info=True):
  def read(v: Atom) -> Any:
    return v.val if isinstance(v, Literal) else env[v]

  def write(v: Var, val: Any) -> None:
    if config.jax_enable_checks and not config.jax_dynamic_shapes:
      assert typecheck(v.aval, val), (v.aval, val)
    env[v] = val

  env: dict[Var, Any] = {}
  map(write, jaxpr.constvars, consts)
  map(write, jaxpr.invars, args)
  lu = last_used(jaxpr)
  for eqn in jaxpr.eqns:
    subfuns, bind_params = eqn.primitive.get_bind_params(eqn.params)
    name_stack = source_info_util.current_name_stack() + eqn.source_info.name_stack
    traceback = eqn.source_info.traceback if propagate_source_info else None
    with source_info_util.user_context(traceback, name_stack=name_stack):
      ans = eqn.primitive.bind(*subfuns, *map(read, eqn.invars), **bind_params)
    if eqn.primitive.multiple_results:
      map(write, eqn.outvars, ans)
    else:
      write(eqn.outvars[0], ans)
    clean_up_dead_vars(eqn, env, lu)
  return map(read, jaxpr.outvars)
