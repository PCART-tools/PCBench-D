def _jvp(fun: lu.WrappedFun, primals, tangents, has_aux=False):
  """Variant of jvp() that takes an lu.WrappedFun."""
  if (not isinstance(primals, (tuple, list)) or
      not isinstance(tangents, (tuple, list))):
    raise TypeError("primal and tangent arguments to jax.jvp must be tuples or lists; "
                    f"found {type(primals).__name__} and {type(tangents).__name__}.")

  ps_flat, tree_def = tree_flatten(primals)
  ts_flat, tree_def_2 = tree_flatten(tangents)
  if tree_def != tree_def_2:
    raise TypeError("primal and tangent arguments to jax.jvp must have the same tree "
                    f"structure; primals have tree structure {tree_def} whereas tangents have "
                    f"tree structure {tree_def_2}.")
  for p, t in safe_zip(ps_flat, ts_flat):
    if core.primal_dtype_to_tangent_dtype(_dtype(p)) != _dtype(t):
      raise TypeError("primal and tangent arguments to jax.jvp do not match; "
                      "dtypes must be equal, or in case of int/bool primal dtype "
                      "the tangent dtype must be float0."
                      f"Got primal dtype {_dtype(p)} and so expected tangent dtype "
                      f"{core.primal_dtype_to_tangent_dtype(_dtype(p))}, but got "
                      f"tangent dtype {_dtype(t)} instead.")
    if np.shape(p) != np.shape(t):
      raise ValueError("jvp called with different primal and tangent shapes;"
                       f"Got primal shape {np.shape(p)} and tangent shape as {np.shape(t)}")

  if not has_aux:
    flat_fun, out_tree = flatten_fun_nokwargs(fun, tree_def)
    out_primals, out_tangents = ad.jvp(flat_fun).call_wrapped(ps_flat, ts_flat)
    out_tree = out_tree()
    return (tree_unflatten(out_tree, out_primals),
            tree_unflatten(out_tree, out_tangents))
  else:
    flat_fun, out_aux_trees = flatten_fun_nokwargs2(fun, tree_def)
    jvp_fun, aux = ad.jvp(flat_fun, has_aux=True)
    out_primals, out_tangents = jvp_fun.call_wrapped(ps_flat, ts_flat)
    out_tree, aux_tree = out_aux_trees()
    return (tree_unflatten(out_tree, out_primals),
            tree_unflatten(out_tree, out_tangents),
            tree_unflatten(aux_tree, aux()))
