@util._wraps(np.tril_indices_from)
def tril_indices_from(arr: ArrayLike, k: int = 0) -> tuple[Array, Array]:
  arr_shape = shape(arr)
  return tril_indices(arr_shape[-2], k=k, m=arr_shape[-1])
