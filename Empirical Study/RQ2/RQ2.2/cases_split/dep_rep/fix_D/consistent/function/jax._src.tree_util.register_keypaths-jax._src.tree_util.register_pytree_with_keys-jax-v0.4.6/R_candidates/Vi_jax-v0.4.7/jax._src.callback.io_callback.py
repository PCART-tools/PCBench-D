def io_callback(callback: Callable[..., Any], result_shape_dtypes: Any,
                *args: Any, ordered: bool = False, **kwargs: Any):
  def _flat_callback(*flat_args):
    args, kwargs = tree_util.tree_unflatten(in_tree, flat_args)
    return tree_util.tree_leaves(callback(*args, **kwargs))

  flat_args, in_tree = tree_util.tree_flatten((args, kwargs))
  tree_util.tree_map(_check_shape_dtype, result_shape_dtypes)
  flat_shape_dtypes, out_tree = tree_util.tree_flatten(result_shape_dtypes)
  flat_result_avals = map(lambda x: core.ShapedArray(x.shape, x.dtype),
                          flat_shape_dtypes)
  flat_args = map(core.raise_as_much_as_possible, flat_args)
  out_flat = io_callback_p.bind(
      *flat_args, callback=_flat_callback,
      result_avals=tuple(flat_result_avals),
      ordered=ordered)
  return tree_util.tree_unflatten(out_tree, out_flat)
