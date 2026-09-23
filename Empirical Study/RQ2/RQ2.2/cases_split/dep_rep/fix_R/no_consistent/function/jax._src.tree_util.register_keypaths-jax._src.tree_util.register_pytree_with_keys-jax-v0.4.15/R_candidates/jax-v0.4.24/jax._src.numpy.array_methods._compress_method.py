def _compress_method(a: ArrayLike, condition: ArrayLike,
                     axis: int | None = None, out: None = None) -> Array:
  """Return selected slices of this array along given axis.

  Refer to :func:`jax.numpy.compress` for full documentation."""
  return lax_numpy.jaxcompress(condition, a, axis, out)
