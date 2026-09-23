def _householder_product_lowering_rule(ctx, a, taus):
  aval_out, = ctx.avals_out
  if not is_constant_shape(aval_out.shape):
    result_shapes = [
        mlir.eval_dynamic_shape_as_tensor(ctx, aval_out.shape)]
  else:
    result_shapes = None
  op = mlir.custom_call(
      "ProductOfElementaryHouseholderReflectors",
      result_types=[mlir.aval_to_ir_type(aval_out)],
      operands=[a, taus],
      api_version=1,
      result_shapes=result_shapes)
  return [op.result]
