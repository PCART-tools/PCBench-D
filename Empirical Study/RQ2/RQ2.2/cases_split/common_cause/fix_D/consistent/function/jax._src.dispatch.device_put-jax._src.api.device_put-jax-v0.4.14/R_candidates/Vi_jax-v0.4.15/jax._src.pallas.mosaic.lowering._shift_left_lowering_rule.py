def _shift_left_lowering_rule(ctx: LoweringRuleContext, x, d):
  if isinstance(x, (np.generic, np.ndarray, int)):
    x = ir_constant(x)
  if isinstance(d, (np.generic, np.ndarray, int)):
    d = ir_constant(d)
  return arith.ShLIOp(x, d).result
