@util.implements(np.column_stack)
def column_stack(tup: np.ndarray | Array | Sequence[ArrayLike]) -> Array:
  arrs: Array | list[Array] | np.ndarray
  if isinstance(tup, (np.ndarray, Array)):
    arrs = jax.vmap(lambda x: atleast_2d(x).T)(tup) if tup.ndim < 3 else tup
  else:
    # TODO(jakevdp): Non-array input deprecated 2023-09-22; change to error.
    util.check_arraylike("column_stack", *tup, emit_warning=True)
    arrs = [atleast_2d(arr).T if arr.ndim < 2 else arr for arr in map(asarray, tup)]
  return concatenate(arrs, 1)
