def _clip(number: ArrayLike,
          min: Optional[ArrayLike] = None, max: Optional[ArrayLike] = None,  # noqa: F811
          out: None = None) -> Array:
  """Return an array whose values are limited to a specified range.

  Refer to :func:`jax.numpy.clip` for full documentation."""
  return clip(number, a_min=min, a_max=max, out=out)
