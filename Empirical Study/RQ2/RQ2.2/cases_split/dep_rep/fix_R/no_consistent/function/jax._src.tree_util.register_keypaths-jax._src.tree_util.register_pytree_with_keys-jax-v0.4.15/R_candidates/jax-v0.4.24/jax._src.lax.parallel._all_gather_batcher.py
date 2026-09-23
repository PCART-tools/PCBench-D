def _all_gather_batcher(vals_in, dims_in, *, all_gather_dimension, axis_name, axis_index_groups, axis_size, tiled):
  (x,), (d,) = vals_in, dims_in
  if d <= all_gather_dimension:
    all_gather_dimension += 1
  elif not tiled:  # Tiled all-gather doesn't modify the set of dimensions
    d += 1
  result = all_gather_p.bind(
      x,
      all_gather_dimension=all_gather_dimension,
      axis_name=axis_name,
      axis_index_groups=axis_index_groups,
      axis_size=axis_size,
      tiled=tiled)
  return result, d
