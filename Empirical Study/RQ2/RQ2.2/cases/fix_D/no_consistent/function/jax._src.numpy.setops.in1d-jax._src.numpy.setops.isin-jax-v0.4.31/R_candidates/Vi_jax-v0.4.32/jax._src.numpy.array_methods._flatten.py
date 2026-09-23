def _flatten(self: Array, order: str = "C") -> Array:
  """Flatten array into a 1-dimensional shape.

  Refer to :func:`jax.numpy.ravel` for the full documentation.
  """
  return lax_numpy.ravel(self, order=order)
