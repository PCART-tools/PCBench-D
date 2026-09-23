def _all(self: Array, axis: reductions.Axis = None, out: None = None,
         keepdims: bool = False, *, where: ArrayLike | None = None) -> Array:
  """Test whether all array elements along a given axis evaluate to True.

  Refer to :func:`jax.numpy.all` for the full documentation.
  """
  return reductions.all(self, axis=axis, out=out, keepdims=keepdims, where=where)
