def _dynamic_update_slice_lower(ctx, x, update, *start_indices):
  aval_out, = ctx.avals_out
  return mhlo.DynamicUpdateSliceOp(mlir.aval_to_ir_type(aval_out), x, update,
                                   start_indices).results
