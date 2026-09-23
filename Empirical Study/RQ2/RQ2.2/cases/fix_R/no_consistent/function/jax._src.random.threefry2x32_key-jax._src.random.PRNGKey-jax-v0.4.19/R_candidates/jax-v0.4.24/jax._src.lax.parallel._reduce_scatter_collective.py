def _reduce_scatter_collective(frame_size, frame_name, _, vals_in, dims_in,
                               scatter_dimension, axis_name,
                               axis_index_groups, axis_size, tiled):
  if axis_index_groups is not None:
    raise NotImplementedError("axis_index_groups not supported in vmap")
  assert axis_size == frame_size, "axis size doesn't match"
  if not isinstance(axis_name, tuple):
    axis_name = (axis_name,)
  if len(axis_name) > 1:
    raise NotImplementedError("Please open a feature request!")
  assert axis_name == (frame_name,), "batcher called with wrong axis name"
  (x,), (d,) = vals_in, dims_in
  if d is batching.not_mapped:
    y, dy = x * axis_size, scatter_dimension
  else:
    y, dy = lax.reduce(x, 0., lax.add, (d,)), scatter_dimension
  if tiled:
    y = _splitaxis(dy, axis_size, y)
  return y, dy
