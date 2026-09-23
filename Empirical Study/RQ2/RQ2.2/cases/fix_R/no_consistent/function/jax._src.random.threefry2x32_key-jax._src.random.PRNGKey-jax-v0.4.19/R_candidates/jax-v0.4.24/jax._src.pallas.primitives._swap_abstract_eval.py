def _swap_abstract_eval(*avals_flat, args_tree, **_):
  ref, indexers, val, _ = args_tree.unflatten(avals_flat)
  expected_output_shape = indexers[-1].get_indexer_shape()
  if expected_output_shape != val.shape:
    raise ValueError(
        f"Invalid shape for `swap`. Ref shape: {ref.shape}. "
        f"Value shape: {val.shape}. Indices: {indexers}. "
    )
  if ref.dtype != val.dtype:
    raise ValueError(
        f"Invalid dtype for `swap`. Ref dtype: {ref.dtype}. "
        f"Value dtype: {val.dtype}. "
    )
  return (
      jax_core.ShapedArray(expected_output_shape, ref.dtype),
      {state.WriteEffect(0)},
  )
