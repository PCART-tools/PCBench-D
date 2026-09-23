def _reduction_batcher(prim, vals_in, dims_in, *, axes, axis_index_groups):
  assert prim.multiple_results
  if not any(isinstance(axis, int) for axis in axes):
    return prim.bind(*vals_in, axes=axes, axis_index_groups=axis_index_groups), dims_in
  vals_out = _reduction_with_positional_batcher(
      prim, vals_in, dims_in, axis_index_groups,
      lambda d, d_vals_in: (axes, d_vals_in),
      lambda d, d_vals_in: (tuple(axis + (axis >= d) if isinstance(axis, int) else axis
                                  for axis in axes),
                            d_vals_in))
  # _reduction_with_positional_batcher moves all map dims to 0
  return vals_out, [d if d is batching.not_mapped else 0 for d in dims_in]
