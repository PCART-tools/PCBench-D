def _iota_lower(ctx, *dyn_shape, dtype, shape, dimension):
  del dtype
  aval_out, = ctx.avals_out
  if dyn_shape:
    shape = _merge_dyn_shape(shape, dyn_shape)
    return mhlo.DynamicIotaOp(
        mlir.aval_to_ir_type(aval_out),
        mlir.shape_tensor(shape),
        mlir.i64_attr(dimension),
    ).results
  else:
    return mhlo.IotaOp(mlir.aval_to_ir_type(aval_out),
                       mlir.i64_attr(dimension)).results
