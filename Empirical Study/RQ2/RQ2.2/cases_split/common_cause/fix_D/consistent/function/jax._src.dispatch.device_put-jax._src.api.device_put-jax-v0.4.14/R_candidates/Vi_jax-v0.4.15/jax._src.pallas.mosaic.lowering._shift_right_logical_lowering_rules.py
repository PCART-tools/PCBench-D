def _shift_right_logical_lowering_rules(ctx: LoweringRuleContext, x, d):
  if isinstance(x, (np.generic, np.ndarray, int)):
    x = ir_constant(x)
  if isinstance(d, (np.generic, np.ndarray, int)):
    d = ir_constant(d)
  return arith.ShRUIOp(x, d).result
