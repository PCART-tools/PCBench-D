def _xor_lowering_rule(ctx: LoweringRuleContext, x, y):
  if isinstance(x, (np.generic, np.ndarray, int, float)):
    x = ir_constant(x)
  if isinstance(y, (np.generic, np.ndarray, int, float)):
    y = ir_constant(y)
  return arith.XOrIOp(x, y).result
