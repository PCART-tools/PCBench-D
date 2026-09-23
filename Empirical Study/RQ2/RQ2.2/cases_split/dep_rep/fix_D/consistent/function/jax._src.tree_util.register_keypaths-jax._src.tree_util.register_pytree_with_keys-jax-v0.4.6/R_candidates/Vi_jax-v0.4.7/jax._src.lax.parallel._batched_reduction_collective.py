def _batched_reduction_collective(
    prim, if_unmapped, axis_size, frame_name, _, vals_in, dims_in, axes,
    axis_index_groups):
  assert prim.multiple_results
  assert frame_name in axes
  # Note that we have a choice here. We can either unfuse the reduction into one
  # that handles the batched dims and then another one that handles the rest.
  # Alternatively, we can keep the dimension reduction fused with the rest, but
  # we have to split the primitive into one for unmapped inputs and another
  # one for mapped, because they differ in their `axes` parameter.
  # We choose the second strategy here.
  vals_out = _reduction_with_positional_batcher(
      prim, vals_in, dims_in, axis_index_groups,
      lambda d, d_vals_in: (tuple(axis for axis in axes if axis != frame_name),
                            [if_unmapped(v, axis_size) for v in d_vals_in]),
      lambda d, d_vals_in: (tuple(axis + (axis >= d) if isinstance(axis, int) else
                                  axis if axis != frame_name else
                                  d
                                  for axis in axes),
                            d_vals_in))
  return vals_out, [batching.not_mapped] * len(vals_out)
