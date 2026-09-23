def _repeat(self: Array, repeats: ArrayLike, axis: int | None = None, *,
            total_repeat_length: int | None = None) -> Array:
  """Construct an array from repeated elements.

  Refer to :func:`jax.numpy.repeat` for the full documentation.
  """
  return lax_numpy.repeat(self, repeats=repeats, axis=axis, total_repeat_length=total_repeat_length)
