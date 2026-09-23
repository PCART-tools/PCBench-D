@util._wraps(np.column_stack)
def column_stack(tup: Union[np.ndarray, Array, Sequence[ArrayLike]]) -> Array:
  if isinstance(tup, (np.ndarray, Array)):
    arrs = jax.vmap(lambda x: atleast_2d(x).T)(tup) if tup.ndim < 3 else tup
  else:
    arrs = [atleast_2d(arr).T if arr.ndim < 2 else arr for arr in map(asarray, tup)]
  return concatenate(arrs, 1)
