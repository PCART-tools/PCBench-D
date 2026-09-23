def _convert_element_type_lowering_rule(
    ctx: TritonLoweringRuleContext, a, *, new_dtype, weak_type
):
  if new_dtype == ctx.avals_in[0].dtype:
    return a
  return tc.semantic.cast(a, _convert_dtype(new_dtype))
