def _argmin(self: Array, axis: int | None = None, out: None = None,
            keepdims: bool | None = None) -> Array:
  """Return the index of the minimum value.

  Refer to :func:`jax.numpy.argmin` for the full documentation.
  """
  return lax_numpy.argmin(self, axis=axis, out=out, keepdims=keepdims)
