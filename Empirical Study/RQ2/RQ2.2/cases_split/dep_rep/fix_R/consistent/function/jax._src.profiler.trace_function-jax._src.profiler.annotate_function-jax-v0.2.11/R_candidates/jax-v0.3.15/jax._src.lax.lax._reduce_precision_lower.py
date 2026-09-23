def _reduce_precision_lower(ctx, operand, *, exponent_bits, mantissa_bits):
  aval_out, = ctx.avals_out
  return mhlo.ReducePrecisionOp(operand, mlir.i32_attr(exponent_bits),
                                mlir.i32_attr(mantissa_bits)).results
