@partial(jit, static_argnames=['return_indices'])
def _intersect1d_sorted_mask(ar1: ArrayLike, ar2: ArrayLike, return_indices: bool = False) -> tuple[Array, ...]:
  """
    Helper function for intersect1d which is jit-able
    """
  ar = concatenate((ar1, ar2))
  if return_indices:
    iota = lax.broadcasted_iota(np.int64, np.shape(ar), dimension=0)
    aux, indices = lax.sort_key_val(ar, iota)
  else:
    aux = sort(ar)

  mask = aux[1:] == aux[:-1]
  if return_indices:
    return aux, mask, indices
  else:
    return aux, mask
