def _platform_index_lowering(ctx: mlir.LoweringRuleContext,
                             *,
                             platforms: Sequence[Sequence[str]],
                             has_default: bool):
  def lower_constant(ctx: mlir.LoweringRuleContext, *, i: int) -> mlir.ir.Value:
    return mlir.ir_constants(np.int32(i))
  platform_rules: dict[str, mlir.LoweringRule] = {}
  for i, ps in enumerate(platforms):
    rule = partial(lower_constant, i=i)
    for p in ps:
      platform_rules[p] = rule

  default_rule = (
    partial(lower_constant, i=len(platforms)) if has_default else None)
  return mlir.lower_per_platform(
    ctx,
    f"platform_index(platforms={platforms}, has_default={has_default})",
    platform_rules, default_rule, effects.no_effects)
