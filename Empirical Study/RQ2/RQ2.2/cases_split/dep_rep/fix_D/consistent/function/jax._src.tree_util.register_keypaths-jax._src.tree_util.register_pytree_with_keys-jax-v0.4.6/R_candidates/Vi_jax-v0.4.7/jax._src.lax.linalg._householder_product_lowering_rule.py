def _householder_product_lowering_rule(ctx, a, taus):
  op = hlo.CustomCallOp(
      [mlir.aval_to_ir_type(ctx.avals_out[0])],
      [a, taus],
      call_target_name=ir.StringAttr.get("ProductOfElementaryHouseholderReflectors"),
      has_side_effect=ir.BoolAttr.get(False),
      api_version=mlir.i32_attr(1),
  )
  return [op.result]
