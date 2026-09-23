def _lu_pivots_to_permutation_gpu_lowering(lowering, ctx, pivots, *,
                                           permutation_size):
  return [lowering(pivots, permutation_size=permutation_size)]
