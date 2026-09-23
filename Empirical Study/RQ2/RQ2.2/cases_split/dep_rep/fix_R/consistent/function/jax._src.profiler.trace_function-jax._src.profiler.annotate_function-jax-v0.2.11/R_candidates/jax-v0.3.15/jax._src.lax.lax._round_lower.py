def _round_lower(ctx, x, *, rounding_method):
  if rounding_method is RoundingMethod.AWAY_FROM_ZERO:
    return mhlo.RoundOp(x).results
  else:
    assert rounding_method is RoundingMethod.TO_NEAREST_EVEN
    round_nearest = mlir.cache_lowering(mlir.lower_fun(_round_to_nearest_even,
                                                       multiple_results=False))
    return round_nearest(ctx, x)
