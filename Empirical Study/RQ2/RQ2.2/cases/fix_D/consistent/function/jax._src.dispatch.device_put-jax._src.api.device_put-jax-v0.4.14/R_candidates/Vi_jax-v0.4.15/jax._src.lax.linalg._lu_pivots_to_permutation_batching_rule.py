def _lu_pivots_to_permutation_batching_rule(batched_args, batch_dims, *,
                                            permutation_size):
  x, = batched_args
  bd, = batch_dims
  x = batching.moveaxis(x, bd, 0)
  return lu_pivots_to_permutation_p.bind(
      x, permutation_size=permutation_size), 0
