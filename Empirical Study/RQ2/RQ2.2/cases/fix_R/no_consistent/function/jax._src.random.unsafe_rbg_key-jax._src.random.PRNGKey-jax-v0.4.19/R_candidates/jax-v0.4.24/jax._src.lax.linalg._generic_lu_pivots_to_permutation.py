def _generic_lu_pivots_to_permutation(swaps, permutation_size):
  """Converts the pivots (row swaps) returned by LU to a permutation.

  We build a permutation rather than applying `swaps` directly to the rows
  of a matrix because lax loops aren't differentiable.

  Args:
    swaps: an array of shape (..., k) of row swaps to perform
    permutation_size: the size of the output permutation. Should be >= k.
  Returns:
    An int32 array of shape (..., m).
  """
  assert len(swaps.shape) >= 1
  batch_dims = swaps.shape[:-1]
  k = swaps.shape[-1]
  m = permutation_size

  permutation = lax.broadcasted_iota(jnp.int32, batch_dims + (m,),
                                     len(batch_dims))
  if m == 0:
    return permutation
  result, _ = lax.fori_loop(np.array(0, np.int32), np.array(k, np.int32),
                            _lu_pivots_body_fn, (permutation, swaps))
  return result
