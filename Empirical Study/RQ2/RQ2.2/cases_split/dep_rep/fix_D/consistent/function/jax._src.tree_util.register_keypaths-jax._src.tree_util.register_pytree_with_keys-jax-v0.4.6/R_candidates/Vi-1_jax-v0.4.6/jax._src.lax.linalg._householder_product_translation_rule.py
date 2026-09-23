def _householder_product_translation_rule(ctx, avals_in, avals_out, a, taus):
  return [xops.ProductOfElementaryHouseholderReflectors(a, taus)]
