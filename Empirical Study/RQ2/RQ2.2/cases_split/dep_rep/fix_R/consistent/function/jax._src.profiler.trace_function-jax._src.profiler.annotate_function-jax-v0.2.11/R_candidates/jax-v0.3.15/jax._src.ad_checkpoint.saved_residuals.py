def saved_residuals(f, *args, **kwargs) -> List[Tuple[core.AbstractValue, str]]:
  args, in_tree = tree_flatten((args, kwargs))

  def f_(*args):
    args, kwargs = tree_unflatten(in_tree, args)
    return f(*args, **kwargs)

  jaxpr = jax.make_jaxpr(lambda *args: jax.linearize(f_, *args)[1])(*args).jaxpr
  res_lits = [x for x in jaxpr.outvars if     isinstance(x, core.Literal)]
  res_vars = {x for x in jaxpr.outvars if not isinstance(x, core.Literal)}

  results = []

  for x in res_lits:
    results.append((x.aval, 'from a literal'))

  for v in jaxpr.constvars:
    if v in res_vars:
      results.append((v.aval, 'from a constant'))

  assert len(jaxpr.invars) == len(args)
  for i, v in enumerate(jaxpr.invars):
    if v in res_vars:
      src = f'from {pe.arg_info_pytree(f, in_tree, True, [i])}'
      results.append((v.aval, src))

  for eqn in jaxpr.eqns:
    src = source_info_util.summarize(eqn.source_info)
    for v in eqn.outvars:
      if v in res_vars:
        if eqn.primitive is name_p:
          results.append((v.aval, f"named '{eqn.params['name']}' from {src}"))
        else:
          results.append((v.aval, f'from {src}'))

  assert len(results) == len(jaxpr.outvars)
  return results
