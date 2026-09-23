def _argmax(self: Array, axis: int | None = None, out: None = None,
            keepdims: bool | None = None) -> Array:
  """Return the index of the maximum value.

  Refer to :func:`jax.numpy.argmax` for the full documentation.
  """
  return lax_numpy.argmax(self, axis=axis, out=out, keepdims=keepdims)
