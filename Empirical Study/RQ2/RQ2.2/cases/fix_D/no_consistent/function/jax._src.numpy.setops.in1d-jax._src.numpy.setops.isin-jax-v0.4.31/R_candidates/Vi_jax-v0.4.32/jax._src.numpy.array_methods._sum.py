def _sum(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
         out: None = None, keepdims: bool = False, initial: ArrayLike | None = None,
         where: ArrayLike | None = None, promote_integers: bool = True) -> Array:
  """Sum of the elements of the array over a given axis.

  Refer to :func:`jax.numpy.sum` for full documentation.
  """
  return reductions.sum(self, axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                        where=where, promote_integers=promote_integers)
