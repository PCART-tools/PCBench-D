@util.implements(np.hstack)
def hstack(tup: np.ndarray | Array | Sequence[ArrayLike],
           dtype: DTypeLike | None = None) -> Array:
  arrs: Array | list[Array]
  if isinstance(tup, (np.ndarray, Array)):
    arrs = jax.vmap(atleast_1d)(tup)
    arr0_ndim = arrs.ndim - 1
  else:
    # TODO(jakevdp): Non-array input deprecated 2023-09-22; change to error.
    util.check_arraylike("hstack", *tup, emit_warning=True)
    arrs = [atleast_1d(m) for m in tup]
    arr0_ndim = arrs[0].ndim
  return concatenate(arrs, axis=0 if arr0_ndim == 1 else 1, dtype=dtype)
