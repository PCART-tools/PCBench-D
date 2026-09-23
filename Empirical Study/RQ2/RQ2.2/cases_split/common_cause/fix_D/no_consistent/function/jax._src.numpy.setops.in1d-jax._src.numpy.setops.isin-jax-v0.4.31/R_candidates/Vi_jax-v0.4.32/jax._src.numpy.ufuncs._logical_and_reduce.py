def _logical_and_reduce(a: ArrayLike, axis: int = 0, dtype: DTypeLike | None = None,
                        out: None = None, keepdims: bool = False, initial: ArrayLike | None = None,
                        where: ArrayLike | None = None):
  if initial is not None:
    raise ValueError("initial argument not supported in jnp.logical_and.reduce()")
  result = reductions.all(a, axis=axis, out=out, keepdims=keepdims, where=where)
  return result if dtype is None else result.astype(dtype)
