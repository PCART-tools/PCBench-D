def _squeeze(self: Array, axis: reductions.Axis = None) -> Array:
  """Remove one or more length-1 axes from array.

  Refer to :func:`jax.numpy.squeeze` for full documentation.
  """
  return lax_numpy.squeeze(self, axis=axis)
