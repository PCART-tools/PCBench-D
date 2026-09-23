def _all_gather_batched_collective(frame_size, frame_name, _, vals_in, dims_in,
                                   all_gather_dimension, axis_name,
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
    out_shape = list(np.shape(x))
    out_shape.insert(all_gather_dimension, axis_size)
    broadcast_dims = [i for i in range(len(out_shape)) if i != all_gather_dimension]
    y = lax.broadcast_in_dim(x, out_shape, broadcast_dims)
  else:
    y = _moveaxis(d, all_gather_dimension, x)
  if tiled:
    y = _foldaxis(all_gather_dimension, y)
  return y, batching.not_mapped
