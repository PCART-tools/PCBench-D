def _dynamic_slice_lower(ctx, x, *starts_and_dyn_sizes, slice_sizes):
  x_aval, *_ = ctx.avals_in
  start_indices, dyn = util.split_list(starts_and_dyn_sizes, [x_aval.ndim])
  aval_out, = ctx.avals_out
  if dyn:
    aval_out = aval_out.update(shape=lax._merge_dyn_shape(slice_sizes, dyn))
  return [mlir.dynamic_slice(ctx, aval_out, x, start_indices=start_indices)]
