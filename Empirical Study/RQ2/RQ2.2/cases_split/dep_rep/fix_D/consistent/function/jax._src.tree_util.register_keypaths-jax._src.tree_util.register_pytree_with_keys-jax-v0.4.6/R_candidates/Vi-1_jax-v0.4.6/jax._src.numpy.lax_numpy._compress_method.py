def _compress_method(a: ArrayLike, condition: ArrayLike,
                     axis: Optional[int] = None, out: None = None) -> Array:
  """Return selected slices of this array along given axis.

  Refer to :func:`jax.numpy.compress` for full documentation."""
  return compress(condition, a, axis, out)
