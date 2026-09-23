def _swap_abstract_eval(ref_aval, val_aval, *all_avals, args_tree,
                        **_: Any):
  idx_aval, *_ = tree_util.tree_unflatten(args_tree, all_avals)
  expected_output_shape = idx_aval.get_indexer_shape()
  if expected_output_shape != val_aval.shape:
    raise ValueError("Invalid shape for `swap`. "
                     f"Ref shape: {ref_aval.shape}. "
                     f"Value shape: {val_aval.shape}. "
                     f"Indices: {idx_aval}. ")
  if ref_aval.dtype != val_aval.dtype:
    raise ValueError("Invalid dtype for `swap`. "
                     f"Ref dtype: {ref_aval.dtype}. "
                     f"Value shape: {val_aval.dtype}. ")
  return (jax_core.ShapedArray(expected_output_shape, ref_aval.dtype),
          {state.WriteEffect(0)})
