def _getslice_lower(ctx, x, lo, hi):
  aval_out, = ctx.avals_out
  return mhlo.RealDynamicSliceOp(
      mlir.aval_to_ir_type(aval_out), x,
      mlir.shape_tensor([lo]), mlir.shape_tensor([hi]), mlir.shape_tensor([1])
  ).results
