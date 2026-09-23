@util._wraps(np.triu_indices_from)
def triu_indices_from(arr: ArrayLike, k: int = 0) -> Tuple[Array, Array]:
  arr_shape = shape(arr)
  return triu_indices(arr_shape[-2], k=k, m=arr_shape[-1])
