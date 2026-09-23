def _lu_tpu_lowering_rule(ctx, operand):

  op = hlo.CustomCallOp(
      [ir.TupleType.get_tuple([mlir.aval_to_ir_type(ctx.avals_out[0]),
                               mlir.aval_to_ir_type(ctx.avals_out[1]),
                               mlir.aval_to_ir_type(ctx.avals_out[2])])],
      [operand],
      call_target_name=ir.StringAttr.get("LuDecomposition"),
      has_side_effect=ir.BoolAttr.get(False),
  )
  return (
      hlo.GetTupleElementOp(op, 0).result,
      hlo.GetTupleElementOp(op, 1).result,
      hlo.GetTupleElementOp(op, 2).result,
  )
