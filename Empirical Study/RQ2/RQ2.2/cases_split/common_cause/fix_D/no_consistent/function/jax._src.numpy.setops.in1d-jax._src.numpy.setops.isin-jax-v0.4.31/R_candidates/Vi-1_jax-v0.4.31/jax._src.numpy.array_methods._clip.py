def _clip(number: ArrayLike,
          min: ArrayLike | None = None, max: ArrayLike | None = None) -> Array:
  """Return an array whose values are limited to a specified range.

  Refer to :func:`jax.numpy.clip` for full documentation."""
  return lax_numpy.clip(number, min=min, max=max)
