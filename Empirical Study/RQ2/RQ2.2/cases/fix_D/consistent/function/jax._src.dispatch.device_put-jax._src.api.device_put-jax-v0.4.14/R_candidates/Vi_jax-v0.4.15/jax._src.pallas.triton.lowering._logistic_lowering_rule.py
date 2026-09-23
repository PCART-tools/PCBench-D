def _logistic_lowering_rule(ctx: TritonLoweringRuleContext, a):
  one_ = tl.core._to_tensor(1.0, ctx.builder)
  x = tl.exp(a.__neg__(_builder=ctx.builder), _builder=ctx.builder)
  x = x.__add__(one_, _builder=ctx.builder)
  x = one_.__truediv__(x, _builder=ctx.builder)
  return x
