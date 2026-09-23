def _top_k_lower(ctx, operand, k):
  if not core.is_constant_dim(k):
    # TODO: https://github.com/openxla/stablehlo/issues/1396
    raise ValueError("native serialization with shape polymorphism not implemented for top_k")
  return chlo.TopKOp(operand, mlir.i64_attr(k)).results
