def saved_residuals(f, *args, **kwargs) -> List[Tuple[core.AbstractValue, str]]:
  in_leaves, in_tree = tree_flatten((args, kwargs))

  def f_(*args):
    args, kwargs = tree_unflatten(in_tree, args)
    return f(*args, **kwargs)

  out = jax.make_jaxpr(lambda *args: jax.linearize(f_, *args)[1],
                       return_shape=True)(*in_leaves)
  assert isinstance(out, tuple)
  jaxpr_, out_shape = out
  jaxpr = jaxpr_.jaxpr
  out_tree = lambda: tree_structure(out_shape)
  res_lits = [x for x in jaxpr.outvars if     isinstance(x, core.Literal)]
  res_vars = {x for x in jaxpr.outvars if not isinstance(x, core.Literal)}

  results = []

  for x in res_lits:
    results.append((x.aval, 'from a literal'))

  for v in jaxpr.constvars:
    if v in res_vars:
      results.append((v.aval, 'from a constant'))

  assert len(jaxpr.invars) == len(in_leaves)
  dbg = pe.debug_info(f, in_tree, out_tree, True, "saved_residuals")
  arg_info = pe.arg_info_all(dbg)
  for i, v in enumerate(jaxpr.invars):
    if v in res_vars:
      if arg_info is not None:
        arg_name, arg_path = arg_info[i]
        src = f'from the argument {arg_name}{keystr(arg_path)}'
      else:
        src = 'from the argument at flattened index {i}'
      results.append((v.aval, src))

  for eqn in jaxpr.eqns:
    src = source_info_util.summarize(eqn.source_info)
    for v in eqn.outvars:
      if v in res_vars:
        if eqn.primitive is name_p:
          results.append((v.aval, f"named '{eqn.params['name']}' from {src}"))
        elif str(eqn.primitive) == 'xla_call':
          results.append((v.aval,
                          f"output of jitted function '{eqn.params['name']}' "
                          f"from {src}"))
        else:
          results.append((v.aval, f'output of {eqn.primitive.name} from {src}'))

  assert len(results) == len(jaxpr.outvars)
  return results
