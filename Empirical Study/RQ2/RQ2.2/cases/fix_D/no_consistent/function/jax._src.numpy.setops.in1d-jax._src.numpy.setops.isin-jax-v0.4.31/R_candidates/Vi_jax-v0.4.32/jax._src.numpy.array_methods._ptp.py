def _ptp(self: Array, axis: reductions.Axis = None, out: None = None,
         keepdims: bool = False) -> Array:
  """Return the peak-to-peak range along a given axis.

  Refer to :func:`jax.numpy.ptp` for the full documentation.
  """
  return reductions.ptp(self, axis=axis, out=out, keepdims=keepdims)
