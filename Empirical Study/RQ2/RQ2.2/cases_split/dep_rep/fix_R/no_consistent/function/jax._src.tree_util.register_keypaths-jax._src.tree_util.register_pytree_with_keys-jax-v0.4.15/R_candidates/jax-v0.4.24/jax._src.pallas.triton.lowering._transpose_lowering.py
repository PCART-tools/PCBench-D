def _transpose_lowering(ctx: TritonLoweringRuleContext, a, *, permutation):
  if permutation != (1, 0):
    raise NotImplementedError(permutation)
  return tc.semantic.trans(a)
