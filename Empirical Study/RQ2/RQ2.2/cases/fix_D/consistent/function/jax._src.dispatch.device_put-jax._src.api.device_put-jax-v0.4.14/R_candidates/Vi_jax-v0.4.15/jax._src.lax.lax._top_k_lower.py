def _top_k_lower(ctx, operand, k):
  if core.is_constant_dim(k):
    return chlo.TopKOp(operand, mlir.i64_attr(k)).results
  k_value, = mlir.eval_dynamic_shape_as_vals(ctx, (k,))
  out_values_aval, out_indices_aval, = ctx.avals_out
  return mlir.custom_call(
      "stablehlo.dynamic_top_k",
      result_types=[mlir.aval_to_ir_type(out_values_aval),
       mlir.aval_to_ir_type(out_indices_aval)],
      operands=[operand, k_value]).results
