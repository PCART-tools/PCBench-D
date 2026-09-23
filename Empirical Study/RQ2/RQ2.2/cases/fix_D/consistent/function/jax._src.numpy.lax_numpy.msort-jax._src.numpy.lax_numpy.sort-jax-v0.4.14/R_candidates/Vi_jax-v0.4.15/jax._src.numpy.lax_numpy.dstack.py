@util._wraps(np.dstack)
def dstack(tup: np.ndarray | Array | Sequence[ArrayLike],
           dtype: DTypeLike | None = None) -> Array:
  if isinstance(tup, (np.ndarray, Array)):
    arrs = jax.vmap(atleast_3d)(tup)
  else:
    arrs = [atleast_3d(m) for m in tup]
  return concatenate(arrs, axis=2, dtype=dtype)
