@util._wraps(np.hstack)
def hstack(tup: Union[np.ndarray, Array, Sequence[ArrayLike]],
           dtype: Optional[DTypeLike] = None) -> Array:
  if isinstance(tup, (np.ndarray, Array)):
    arrs = jax.vmap(atleast_1d)(tup)
    arr0_ndim = arrs.ndim - 1
  else:
    arrs = [atleast_1d(m) for m in tup]
    arr0_ndim = arrs[0].ndim
  return concatenate(arrs, axis=0 if arr0_ndim == 1 else 1, dtype=dtype)
