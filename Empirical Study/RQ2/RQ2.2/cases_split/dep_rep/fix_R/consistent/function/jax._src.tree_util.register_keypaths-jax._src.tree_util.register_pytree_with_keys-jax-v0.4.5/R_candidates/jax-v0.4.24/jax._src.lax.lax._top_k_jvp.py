def _top_k_jvp(primals, tangents, *, k):
  operand, = primals
  tangent, = tangents
  primals_out = top_k(operand, k)
  if type(tangent) is ad_util.Zero:
    tangent_out = ad_util.Zero.from_value(primals_out[0])
  else:
    _, k_idxs = primals_out
    idx_shape = k_idxs.shape
    rank = len(idx_shape)
    gather_index_shape = idx_shape + (1,)
    gather_indices = []
    for i in range(rank-1):
      _iota = iota(k_idxs.dtype, idx_shape[i])
      _iota = broadcast_in_dim(_iota, gather_index_shape, (i,))
      gather_indices.append(_iota)
    gather_indices.append(reshape(k_idxs, gather_index_shape))
    gather_indices = concatenate(gather_indices, dimension=rank)
    slice_sizes = (1,) * rank
    dnums = slicing.GatherDimensionNumbers(
      offset_dims=(),
      collapsed_slice_dims=tuple(range(rank)),
      start_index_map=tuple(range(rank)))
    tangent_out = slicing.gather(tangent, gather_indices, dnums, slice_sizes)
  return primals_out, (tangent_out, ad_util.Zero.from_value(primals_out[1]))
