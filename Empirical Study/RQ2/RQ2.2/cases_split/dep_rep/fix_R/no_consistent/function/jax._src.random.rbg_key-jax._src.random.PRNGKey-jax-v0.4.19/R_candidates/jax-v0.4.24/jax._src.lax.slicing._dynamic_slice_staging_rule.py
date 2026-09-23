def _dynamic_slice_staging_rule(trace, x, *starts_and_dyn_sizes, slice_sizes):
  start_indices, dyn = util.split_list(starts_and_dyn_sizes, [x.ndim])
  if not dyn:
    return trace.default_process_primitive(dynamic_slice_p, (x, *start_indices),
                                           dict(slice_sizes=slice_sizes))
  shape = lax._merge_dyn_shape(slice_sizes, dyn)
  aval = core.DShapedArray(shape, x.dtype, False)
  return lax._dyn_shape_staging_rule(trace, dynamic_slice_p, aval, x,
                                     *starts_and_dyn_sizes,
                                     slice_sizes=slice_sizes)
