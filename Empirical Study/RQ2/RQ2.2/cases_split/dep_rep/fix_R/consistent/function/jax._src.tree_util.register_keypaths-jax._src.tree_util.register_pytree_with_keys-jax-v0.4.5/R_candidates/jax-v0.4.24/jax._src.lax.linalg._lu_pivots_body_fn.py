def _lu_pivots_body_fn(i, permutation_and_swaps):
  permutation, swaps = permutation_and_swaps
  batch_dims = swaps.shape[:-1]
  j = swaps[..., i]
  iotas = jnp.ix_(*(lax.iota(jnp.int32, b) for b in batch_dims))
  x = permutation[..., i]
  y = permutation[iotas + (j,)]
  permutation = permutation.at[..., i].set(y)
  return permutation.at[iotas + (j,)].set(x), swaps
