@util._wraps(np.dstack)
def dstack(tup: Union[np.ndarray, Array, Sequence[ArrayLike]],
           dtype: Optional[DTypeLike] = None) -> Array:
  if isinstance(tup, (np.ndarray, Array)):
    arrs = jax.vmap(atleast_3d)(tup)
  else:
    arrs = [atleast_3d(m) for m in tup]
  return concatenate(arrs, axis=2, dtype=dtype)
