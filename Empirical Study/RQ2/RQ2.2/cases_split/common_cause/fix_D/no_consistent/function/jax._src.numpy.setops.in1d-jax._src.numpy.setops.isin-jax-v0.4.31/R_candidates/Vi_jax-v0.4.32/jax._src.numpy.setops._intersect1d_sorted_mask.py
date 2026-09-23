@partial(jit, static_argnames=['return_indices'])
def _intersect1d_sorted_mask(arr1: Array, arr2: Array,
                             return_indices: bool) -> tuple[Array, Array, Array | None]:
  """JIT-compatible helper function for intersect1d"""
  assert arr1.ndim == arr2.ndim == 1
  arr = concatenate((arr1, arr2))
  if return_indices:
    iota = lax.broadcasted_iota(np.int64, np.shape(arr), dimension=0)
    aux, indices = lax.sort_key_val(arr, iota)
  else:
    aux = sort(arr)
    indices = None
  mask = aux[1:] == aux[:-1]
  return aux, mask, indices
