def _prod(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
          out: None = None, keepdims: bool = False,
          initial: ArrayLike | None = None, where: ArrayLike | None = None,
          promote_integers: bool = True) -> Array:
  """Return product of the array elements over a given axis.

  Refer to :func:`jax.numpy.prod` for the full documentation.
  """
  return reductions.prod(self, axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                         initial=initial, where=where, promote_integers=promote_integers)
