def _top_k_translation_rule(ctx, avals_in, avals_out, x, *, k):
  return xla.xla_destructure(ctx.builder, xops.TopK(x, k))
