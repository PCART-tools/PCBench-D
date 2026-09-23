def _transpose_lowering_rule(ctx: LoweringRuleContext, x, *, permutation):
  if permutation != (1, 0):
    raise NotImplementedError
  out_type = aval_to_ir_type(ctx.avals_out[0])
  i64_type = ir.IntegerType.get_signless(64)
  transp = ir.ArrayAttr.get(
      [ir.IntegerAttr.get(i64_type, i) for i in permutation]
  )
  return vector.TransposeOp(out_type, x, transp).result
