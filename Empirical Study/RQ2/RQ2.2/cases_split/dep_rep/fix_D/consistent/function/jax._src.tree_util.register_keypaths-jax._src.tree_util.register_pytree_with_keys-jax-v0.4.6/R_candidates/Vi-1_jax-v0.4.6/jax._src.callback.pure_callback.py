def pure_callback(callback: Callable[..., Any], result_shape_dtypes: Any,
                  *args: Any, vectorized: bool = False, **kwargs: Any):
  def _flat_callback(*flat_args):
    args, kwargs = tree_util.tree_unflatten(in_tree, flat_args)
    return tree_util.tree_leaves(callback(*args, **kwargs))

  flat_args, in_tree = tree_util.tree_flatten((args, kwargs))
  tree_util.tree_map(_check_shape_dtype, result_shape_dtypes)
  result_avals = tree_util.tree_map(
      lambda x: core.ShapedArray(x.shape, x.dtype), result_shape_dtypes)
  flat_result_avals, out_tree = tree_util.tree_flatten(result_avals)
  out_flat = pure_callback_p.bind(
      *flat_args, callback=_flat_callback,
      result_avals=tuple(flat_result_avals), vectorized=vectorized)
  return tree_util.tree_unflatten(out_tree, out_flat)
