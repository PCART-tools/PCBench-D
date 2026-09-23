def _integer_pow_lowering_rule(ctx: TritonLoweringRuleContext, a, *, y):
  if y == 2:
    return a.__mul__(a, _builder=ctx.builder)
  if y == 3:
    return a.__mul__(a.__mul__(a, _builder=ctx.builder), _builder=ctx.builder)
  if y == -2:
    one_ = tl.core._to_tensor(1.0, ctx.builder)
    a_sq = a.__mul__(a, _builder=ctx.builder)
    return one_.__truediv__(a_sq, _builder=ctx.builder)
  return tl.math.pow(a, y, _builder=ctx.builder)
