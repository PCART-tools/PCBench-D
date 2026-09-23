def _reduce_scatter_via_reducer(x, *, reducer, scatter_dimension, axis_name,
                                axis_index_groups, axis_size, tiled):
  index = _index_in_group(axis_name, axis_index_groups)
  scatter_dim_input_size = x.shape[scatter_dimension]
  if tiled and scatter_dim_input_size % axis_size != 0:
    raise ValueError(f"tiled reduce_scatter operand scatter dimension size "
                     f"{scatter_dim_input_size} must be divisible by "
                     f"shard count {axis_size}")
  elif not tiled and scatter_dim_input_size != axis_size:
    raise ValueError(f"reduce_scatter operand scatter dimension size "
                     f"{scatter_dim_input_size} must match shard count"
                     f"{axis_size}")
  scatter_dim_output_size = scatter_dim_input_size // axis_size

  outs = reducer(x, axis_name=axis_name, axis_index_groups=axis_index_groups)
  outs = slicing.dynamic_slice_in_dim(
      outs,
      start_index=index * scatter_dim_output_size,
      slice_size=scatter_dim_output_size,
      axis=scatter_dimension)
  if not tiled:
    outs = lax.squeeze(outs, [scatter_dimension])
  return outs
