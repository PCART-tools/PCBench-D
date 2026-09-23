def _iota_batching_rule(in_vals, in_dims, *, dtype, shape, dimension):
  (segment_lengths,), (ax,) = in_vals, in_dims
  shapes = [_merge_dyn_shape(shape, (d,)) for d in segment_lengths]
  iotas = [broadcasted_iota(dtype, s, dimension) for s in shapes]
  return concatenate(iotas, dimension), batching.ConcatAxis(ax, segment_lengths)
