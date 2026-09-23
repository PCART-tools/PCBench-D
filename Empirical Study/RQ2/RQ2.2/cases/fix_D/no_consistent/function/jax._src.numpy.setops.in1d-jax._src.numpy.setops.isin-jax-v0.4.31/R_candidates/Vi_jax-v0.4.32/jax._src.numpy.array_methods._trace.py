def _trace(self: Array, offset: int | ArrayLike = 0, axis1: int = 0, axis2: int = 1,
           dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Return the sum along the diagonal.

  Refer to :func:`jax.numpy.trace` for full documentation.
  """
  return lax_numpy.trace(self, offset=offset, axis1=axis1, axis2=axis2, dtype=dtype, out=out)
