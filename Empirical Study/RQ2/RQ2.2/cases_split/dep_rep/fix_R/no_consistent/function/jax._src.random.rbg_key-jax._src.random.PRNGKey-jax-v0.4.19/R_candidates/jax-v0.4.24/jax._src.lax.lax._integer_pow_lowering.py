def _integer_pow_lowering(ctx, x, *, y):
  lowering = mlir.lower_fun(_integer_pow, multiple_results=False)
  # TODO(b/217551391): emitting an out-of-line call leads to a large
  # expansion when the MLIR is lowered to HLO, because the HLO lowering
  # clones the callee. Consider unconditionally caching when the MLIR->HLO
  # lowering doesn't expand the program.
  if y >= 4:
    lowering = mlir.cache_lowering(lowering)
  return lowering(ctx, x, y=y)
