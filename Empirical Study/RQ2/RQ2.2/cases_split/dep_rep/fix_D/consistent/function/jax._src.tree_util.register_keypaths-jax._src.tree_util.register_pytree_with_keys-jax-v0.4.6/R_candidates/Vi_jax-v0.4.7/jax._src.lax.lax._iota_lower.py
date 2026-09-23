def _iota_lower(ctx, *dyn_shape, dtype, shape, dimension):
  del dtype
  aval_out, = ctx.avals_out
  if dyn_shape:
    aval_out = aval_out.update(shape=_merge_dyn_shape(shape, dyn_shape))
  if not core.is_constant_shape(aval_out.shape):
    shape = mlir.eval_dynamic_shape(ctx, aval_out.shape)
    return hlo.DynamicIotaOp(
        mlir.aval_to_ir_type(aval_out),
        mlir.shape_tensor(shape),
        mlir.i64_attr(dimension),
    ).results
  else:
    return hlo.IotaOp(mlir.aval_to_ir_type(aval_out),
                      mlir.i64_attr(dimension)).results
