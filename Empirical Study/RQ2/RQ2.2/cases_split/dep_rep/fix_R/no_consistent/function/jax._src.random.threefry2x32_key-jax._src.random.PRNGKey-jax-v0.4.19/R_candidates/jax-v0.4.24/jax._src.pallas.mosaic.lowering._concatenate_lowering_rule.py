def _concatenate_lowering_rule(ctx: LoweringRuleContext, *xs, dimension):
  return tpu.ConcatenateOp(
      aval_to_ir_type(ctx.avals_out[0]), xs, dimension=dimension
  ).result
