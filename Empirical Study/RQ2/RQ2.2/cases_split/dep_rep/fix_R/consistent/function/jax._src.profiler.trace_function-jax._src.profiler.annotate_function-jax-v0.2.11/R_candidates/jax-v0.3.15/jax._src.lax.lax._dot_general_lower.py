def _dot_general_lower(ctx, lhs, rhs, *, dimension_numbers,
                       precision, preferred_element_type: Optional[np.dtype]):
  del preferred_element_type  # Implied by the output aval
  lhs_aval, rhs_aval = ctx.avals_in
  aval_out, = ctx.avals_out
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers

  # TODO(b/195364460): Work around slow XLA/CPU implementation of float16 matmul
  if ctx.module_context.platform == "cpu":
    if lhs_aval.dtype == np.float16:
      f32 = mlir.dtype_to_ir_type(np.dtype(np.float32))
      lhs = mhlo.ConvertOp(ir.RankedTensorType.get(lhs_aval.shape, f32),
                           lhs).result
    if rhs_aval.dtype == np.float16:
      f32 = mlir.dtype_to_ir_type(np.dtype(np.float32))
      rhs = mhlo.ConvertOp(ir.RankedTensorType.get(rhs_aval.shape, f32),
                           rhs).result
  dot_dnums = mhlo.DotDimensionNumbers.get(
      lhs_batching_dimensions=list(lhs_batch),
      rhs_batching_dimensions=list(rhs_batch),
      lhs_contracting_dimensions=list(lhs_contracting),
      rhs_contracting_dimensions=list(rhs_contracting))
  return [
      mhlo.DotGeneralOp(
          mlir.aval_to_ir_type(aval_out),
          lhs,
          rhs,
          dot_dnums,
          precision_config=precision_attr(precision)).result
  ]
