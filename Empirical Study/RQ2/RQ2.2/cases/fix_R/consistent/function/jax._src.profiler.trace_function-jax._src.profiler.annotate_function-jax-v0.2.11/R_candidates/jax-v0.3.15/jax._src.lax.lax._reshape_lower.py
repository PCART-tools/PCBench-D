def _reshape_lower(ctx, x, *dyn_shape, new_sizes, dimensions):
  aval_out, = ctx.avals_out
  if dimensions is not None:
    x = mhlo.TransposeOp(x, mlir.dense_int_elements(dimensions)).result
  if dyn_shape:
    shape = _merge_dyn_shape(new_sizes, dyn_shape)
    return mhlo.DynamicReshapeOp(
        mlir.aval_to_ir_type(aval_out), x,
        mlir.shape_tensor(shape),
    ).results
  else:
    return mhlo.ReshapeOp(mlir.aval_to_ir_type(aval_out), x).results
