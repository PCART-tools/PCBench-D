def _program_id_lowering_rule(ctx: TritonLoweringRuleContext, *, axis):
  return ctx.context.program_ids[axis]
