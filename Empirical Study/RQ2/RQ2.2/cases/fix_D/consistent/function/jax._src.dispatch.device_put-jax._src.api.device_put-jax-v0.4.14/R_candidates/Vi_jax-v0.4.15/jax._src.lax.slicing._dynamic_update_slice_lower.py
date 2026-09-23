def _dynamic_update_slice_lower(ctx, x, update, *start_indices):
  aval_out, = ctx.avals_out
  return [mlir.dynamic_update_slice(ctx, aval_out, x, update,
                                    start_indices=start_indices)]
