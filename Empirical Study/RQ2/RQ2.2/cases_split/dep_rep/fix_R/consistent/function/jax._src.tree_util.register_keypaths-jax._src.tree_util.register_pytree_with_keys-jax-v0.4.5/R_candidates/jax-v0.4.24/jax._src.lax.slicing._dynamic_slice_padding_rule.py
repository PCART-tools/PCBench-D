def _dynamic_slice_padding_rule(in_avals, out_avals, x, *starts_and_dyn,
                                slice_sizes):
  x_aval, start_indices_avals, dyn_avals = util.split_list(in_avals, [1, x.ndim])
  start_indices, dyn = util.split_list(starts_and_dyn, [x.ndim])
  dyn_ = [a.dtype.bound if type(a.dtype) is core.bint else d
          for a, d in zip(dyn_avals, dyn)]
  slice_sizes_ = lax._merge_dyn_shape(slice_sizes, dyn_)
  start_idx = [d.val if type(d) is core.DArray else d for d in start_indices]
  return [dynamic_slice(x, start_idx, slice_sizes_)]
