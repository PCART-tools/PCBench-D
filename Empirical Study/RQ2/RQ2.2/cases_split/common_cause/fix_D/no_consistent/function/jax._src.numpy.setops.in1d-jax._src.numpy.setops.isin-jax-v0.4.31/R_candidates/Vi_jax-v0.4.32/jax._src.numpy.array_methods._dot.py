def _dot(self: Array, b: ArrayLike, *, precision: lax_internal.PrecisionLike = None,
         preferred_element_type: DTypeLike | None = None) -> Array:
  """Compute the dot product of two arrays.

  Refer to :func:`jax.numpy.dot` for the full documentation.
  """
  return lax_numpy.dot(self, b, precision=precision, preferred_element_type=preferred_element_type)
