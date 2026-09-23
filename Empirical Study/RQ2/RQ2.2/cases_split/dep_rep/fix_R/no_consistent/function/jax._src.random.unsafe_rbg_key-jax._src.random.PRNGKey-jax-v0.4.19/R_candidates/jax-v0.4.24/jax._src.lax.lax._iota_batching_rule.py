def _iota_batching_rule(in_vals, in_dims, *, dtype, shape, dimension):
  (segment_lengths,), (ax,) = in_vals, in_dims
  assert ax == 0
  bound = segment_lengths.dtype.bound
  ragged_axis, = (i for i, dim in enumerate(shape) if dim is None)
  shape = (len(segment_lengths),) + _merge_dyn_shape(shape, (bound,))
  iota = broadcasted_iota(dtype, shape, dimension+1)
  return iota, batching.RaggedAxis(ax, ((ragged_axis+1, segment_lengths),))
