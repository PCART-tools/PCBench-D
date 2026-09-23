def _reduction_with_positional_batcher(prim, vals_in, dims_in, axis_index_groups,
    transform_unmapped, transform_mapped):
  if axis_index_groups is not None:
    raise NotImplementedError("axis_index_groups not supported in vmap collectives. "
                              "Please open a feature request!")
  vals_in = [val if d is batching.not_mapped or d == 0 else _moveaxis(d, 0, val)
             for val, d in zip(vals_in, dims_in)]
  mapped_vals_in, unmapped_vals_in = partitioned_vals_in = [], []
  mapped_idxs, unmapped_idxs = partitioned_idxs = [], []
  for i, (val, d) in enumerate(zip(vals_in, dims_in)):
    partitioned_vals_in[d is batching.not_mapped].append(val)
    partitioned_idxs[d is batching.not_mapped].append(i)
  vals_out = [None] * len(vals_in)
  if unmapped_vals_in:
    unmapped_axes, unmapped_vals_in = transform_unmapped(0, unmapped_vals_in)
    unmapped_vals_out = prim.bind(*unmapped_vals_in, axes=unmapped_axes, axis_index_groups=None)
    for i, val in zip(unmapped_idxs, unmapped_vals_out):
      vals_out[i] = val
  if mapped_vals_in:
    mapped_axes, mapped_vals_in = transform_mapped(0, mapped_vals_in)
    mapped_vals_out = prim.bind(*mapped_vals_in, axes=mapped_axes, axis_index_groups=None)
    for i, val in zip(mapped_idxs, mapped_vals_out):
      vals_out[i] = val
  assert all(v is not None for v in vals_out)
  return vals_out
