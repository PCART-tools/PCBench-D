def _bitcast_convert_type_lower(ctx, operand, *, new_dtype):
  aval_out, = ctx.avals_out
  return hlo.BitcastConvertOp(mlir.aval_to_ir_type(aval_out), operand).results
