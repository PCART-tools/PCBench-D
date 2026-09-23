@util.implements(np.dstack)
def dstack(tup: np.ndarray | Array | Sequence[ArrayLike],
           dtype: DTypeLike | None = None) -> Array:
  arrs: Array | list[Array]
  if isinstance(tup, (np.ndarray, Array)):
    arrs = jax.vmap(atleast_3d)(tup)
  else:
    # TODO(jakevdp): Non-array input deprecated 2023-09-22; change to error.
    util.check_arraylike("dstack", *tup, emit_warning=True)
    arrs = [atleast_3d(m) for m in tup]
  return concatenate(arrs, axis=2, dtype=dtype)
