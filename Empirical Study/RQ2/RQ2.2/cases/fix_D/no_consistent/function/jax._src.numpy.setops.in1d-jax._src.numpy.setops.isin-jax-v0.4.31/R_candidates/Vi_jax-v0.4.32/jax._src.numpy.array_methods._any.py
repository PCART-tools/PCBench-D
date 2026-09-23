def _any(self: Array, axis: reductions.Axis = None, out: None = None,
         keepdims: bool = False, *, where: ArrayLike | None = None) -> Array:
  """Test whether any array elements along a given axis evaluate to True.

  Refer to :func:`jax.numpy.any` for the full documentation.
  """
  return reductions.any(self, axis=axis, out=out, keepdims=keepdims, where=where)
