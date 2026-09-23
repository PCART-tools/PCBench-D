def _geqrf_lowering_rule(ctx, operand):
  ts_type = mlir.aval_to_ir_type(ctx.avals_out[0])
  r_type = mlir.aval_to_ir_type(ctx.avals_out[1])
  op = hlo.CustomCallOp(
      [ir.TupleType.get_tuple([ts_type, r_type])],
      [operand],
      call_target_name=ir.StringAttr.get("Qr"),
      has_side_effect=ir.BoolAttr.get(False),
      api_version=mlir.i32_attr(1),
  )
  return (
      hlo.GetTupleElementOp(op, 0).result,
      hlo.GetTupleElementOp(op, 1).result,
  )
