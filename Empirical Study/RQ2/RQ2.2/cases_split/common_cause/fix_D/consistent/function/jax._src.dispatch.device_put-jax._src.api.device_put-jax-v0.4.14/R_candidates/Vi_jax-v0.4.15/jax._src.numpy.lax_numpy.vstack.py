@util._wraps(np.vstack)
def vstack(tup: np.ndarray | Array | Sequence[ArrayLike],
           dtype: DTypeLike | None = None) -> Array:
  if isinstance(tup, (np.ndarray, Array)):
    arrs = jax.vmap(atleast_2d)(tup)
  else:
    arrs = [atleast_2d(m) for m in tup]
  return concatenate(arrs, axis=0, dtype=dtype)
