def _mean(self: Array, axis: reductions.Axis = None, dtype: DTypeLike | None = None,
          out: None = None, keepdims: bool = False, *,
          where: ArrayLike | None = None) -> Array:
  """Return the mean of array elements along a given axis.

  Refer to :func:`jax.numpy.mean` for the full documentation.
  """
  return reductions.mean(self, axis=axis, dtype=dtype, out=out,
                         keepdims=keepdims, where=where)
