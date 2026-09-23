def _clip(self: Array, min: ArrayLike | None = None, max: ArrayLike | None = None) -> Array:
  """Return an array whose values are limited to a specified range.

  Refer to :func:`jax.numpy.clip` for full documentation.
  """
  return lax_numpy.clip(self, min=min, max=max)
