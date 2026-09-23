def _top_k_lower(ctx, operand, k):
  return chlo.TopKOp(operand, mlir.i64_attr(k)).results
