def _all_gather_transpose_rule(cts, x, *, all_gather_dimension, axis_name, axis_index_groups, axis_size, tiled):
  if tiled:
    raise NotImplementedError("Please open a feature request!")
  # TODO(cjfj): Use lax.reduce_scatter here
  concat_axis = 0
  return (lax_numpy.sum(all_to_all(
      cts, axis_name=axis_name, split_axis=all_gather_dimension,
      concat_axis=concat_axis, axis_index_groups=axis_index_groups),
      axis=concat_axis),)
