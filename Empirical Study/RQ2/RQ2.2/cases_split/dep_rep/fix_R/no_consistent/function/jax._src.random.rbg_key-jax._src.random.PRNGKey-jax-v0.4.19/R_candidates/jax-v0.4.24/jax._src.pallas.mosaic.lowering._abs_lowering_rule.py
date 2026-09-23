def _abs_lowering_rule(ctx: LoweringRuleContext, x):
  (aval_out,) = ctx.avals_out
  if jnp.issubdtype(aval_out.dtype, jnp.integer):
    return math.AbsIOp(x).result
  if jnp.issubdtype(aval_out.dtype, jnp.floating):
    return math.AbsFOp(x).result
  raise NotImplementedError(aval_out.dtype)
