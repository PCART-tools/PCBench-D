def saved_residuals(f, *args, **kwargs) -> list[tuple[core.AbstractValue, str]]:
  in_leaves, in_tree = tree_flatten((args, kwargs))

  def f_(*args):
    args, kwargs = tree_unflatten(in_tree, args)
    return f(*args, **kwargs)

  out = api.make_jaxpr(lambda *args: api.linearize(f_, *args)[1],
                       return_shape=True)(*in_leaves)
  assert isinstance(out, tuple)
  jaxpr_, out_shape = out
  jaxpr = jaxpr_.jaxpr
  out_tree = lambda: tree_structure(out_shape)
  assert len(jaxpr.invars) == len(in_leaves)
  dbg = pe.debug_info(f, in_tree, out_tree, True, "saved_residuals")
  arg_info = pe.arg_info_all(dbg)
  return _saved_residuals(jaxpr, arg_info)
