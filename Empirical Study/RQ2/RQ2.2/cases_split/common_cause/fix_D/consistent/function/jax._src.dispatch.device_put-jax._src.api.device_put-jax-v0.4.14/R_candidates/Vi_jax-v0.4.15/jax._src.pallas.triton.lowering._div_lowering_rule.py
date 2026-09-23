def _div_lowering_rule(ctx: TritonLoweringRuleContext, a, b):
  floating_dtypes = {tl.float16, tl.float32, tl.float64, tl.bfloat16}
  if a.dtype in floating_dtypes and b.dtype in floating_dtypes:
    return a.__truediv__(b, _builder=ctx.builder)
  return a.__floordiv__(b, _builder=ctx.builder)
