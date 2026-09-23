@util.implements(np.vstack)
def vstack(tup: np.ndarray | Array | Sequence[ArrayLike],
           dtype: DTypeLike | None = None) -> Array:
  arrs: Array | list[Array]
  if isinstance(tup, (np.ndarray, Array)):
    arrs = jax.vmap(atleast_2d)(tup)
  else:
    # TODO(jakevdp): Non-array input deprecated 2023-09-22; change to error.
    util.check_arraylike("vstack", *tup, emit_warning=True)
    arrs = [atleast_2d(m) for m in tup]
  return concatenate(arrs, axis=0, dtype=dtype)
