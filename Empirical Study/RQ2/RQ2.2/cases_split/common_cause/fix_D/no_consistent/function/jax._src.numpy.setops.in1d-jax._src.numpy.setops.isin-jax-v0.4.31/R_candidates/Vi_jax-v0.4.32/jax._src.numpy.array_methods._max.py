def _max(self: Array, axis: reductions.Axis = None, out: None = None,
         keepdims: bool = False, initial: ArrayLike | None = None,
         where: ArrayLike | None = None) -> Array:
  """Return the maximum of array elements along a given axis.

  Refer to :func:`jax.numpy.max` for the full documentation.
  """
  return reductions.max(self, axis=axis, out=out, keepdims=keepdims,
                        initial=initial, where=where)
