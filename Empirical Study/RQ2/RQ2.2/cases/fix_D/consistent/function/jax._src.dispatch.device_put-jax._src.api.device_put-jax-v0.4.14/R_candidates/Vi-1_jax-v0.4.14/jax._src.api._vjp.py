def _vjp(fun: lu.WrappedFun, *primals, has_aux=False, reduce_axes=()):
  """Variant of vjp() that takes an lu.WrappedFun."""
  primals_flat, in_tree = tree_flatten(primals)
  for arg in primals_flat: dispatch.check_arg(arg)
  if not has_aux:
    flat_fun, out_tree = flatten_fun_nokwargs(fun, in_tree)
    out_primal, out_vjp = ad.vjp(
        flat_fun, primals_flat, reduce_axes=reduce_axes)
    out_tree = out_tree()
  else:
    flat_fun, out_aux_trees = flatten_fun_nokwargs2(fun, in_tree)
    out_primal, out_vjp, aux = ad.vjp(
        flat_fun, primals_flat, has_aux=True, reduce_axes=reduce_axes)
    out_tree, aux_tree = out_aux_trees()
  out_primal_py = tree_unflatten(out_tree, out_primal)
  ct_dtypes = [core.primal_dtype_to_tangent_dtype(_dtype(x)) for x in out_primal]
  ct_shapes = [np.shape(x) for x in out_primal]
  # Ensure that vjp_py is a PyTree so that we can pass it from the forward to the
  # backward pass in a custom VJP.
  vjp_py = Partial(partial(_vjp_pullback_wrapper, fun.__name__,
                           ct_dtypes, ct_shapes, (out_tree, in_tree)),
                   out_vjp)
  if not has_aux:
    return out_primal_py, vjp_py
  else:
    return out_primal_py, vjp_py, tree_unflatten(aux_tree, aux)
