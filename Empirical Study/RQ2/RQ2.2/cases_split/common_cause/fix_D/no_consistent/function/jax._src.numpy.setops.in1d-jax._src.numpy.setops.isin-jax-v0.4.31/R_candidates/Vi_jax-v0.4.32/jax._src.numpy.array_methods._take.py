def _take(self: Array, indices: ArrayLike, axis: int | None = None, out: None = None,
          mode: str | None = None, unique_indices: bool = False, indices_are_sorted: bool = False,
          fill_value: StaticScalar | None = None) -> Array:
  """Take elements from an array.

  Refer to :func:`jax.numpy.take` for full documentation.
  """
  return lax_numpy.take(self, indices, axis=axis, out=out, mode=mode, unique_indices=unique_indices,
                        indices_are_sorted=indices_are_sorted, fill_value=fill_value)
