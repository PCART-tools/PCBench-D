def _exp2_lowering_rule(ctx: LoweringRuleContext, x):
  # exp2 in JAX lowers to exp(ln2 * x), not to pow2. We match that behavior
  # here.
  return lower_fun(lambda x: jnp.exp(np.log(2) * x), multiple_results=False)(
      ctx, x)
