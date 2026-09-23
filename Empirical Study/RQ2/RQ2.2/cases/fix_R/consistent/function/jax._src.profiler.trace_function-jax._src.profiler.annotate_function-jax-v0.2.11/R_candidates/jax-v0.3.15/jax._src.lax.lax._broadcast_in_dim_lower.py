def _broadcast_in_dim_lower(ctx, x, *dyn_shape, shape, broadcast_dimensions):
  aval_out, = ctx.avals_out
  if dyn_shape:
    shape = _merge_dyn_shape(shape, dyn_shape)
    return mhlo.DynamicBroadcastInDimOp(
        mlir.aval_to_ir_type(aval_out), x,
        mlir.shape_tensor(shape),
        mlir.dense_int_elements(broadcast_dimensions),
    ).results
  else:
    return mhlo.BroadcastInDimOp(
        mlir.aval_to_ir_type(aval_out), x,
        mlir.dense_int_elements(broadcast_dimensions)
    ).results
