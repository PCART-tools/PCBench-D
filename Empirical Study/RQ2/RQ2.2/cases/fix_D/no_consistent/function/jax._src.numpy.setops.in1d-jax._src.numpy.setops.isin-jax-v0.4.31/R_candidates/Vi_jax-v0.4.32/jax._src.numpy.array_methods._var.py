def _var(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
         out: None = None, ddof: int = 0, keepdims: bool = False, *,
         where: ArrayLike | None = None, correction: int | float | None = None) -> Array:
  """Compute the variance along a given axis.

  Refer to :func:`jax.numpy.var` for full documentation.
  """
  return reductions.var(self, axis=axis, dtype=dtype, out=out, ddof=ddof,
                        keepdims=keepdims, where=where, correction=correction)
