def _pjit_lowering_rule(ctx: LoweringRuleContext, *args, jaxpr, **_):
  args = [
      a if isinstance(a, ir.Value) else ir_constant(a, aval_to_ir_type(aval))
      for a, aval in zip(args, ctx.avals_in)
  ]
  lowering_context = ctx.lowering_context.replace(block_shapes=ctx.block_shapes)
  return jaxpr_subcomp(lowering_context, jaxpr.jaxpr, *args)
