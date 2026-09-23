def _astype(arr: ArrayLike, dtype: DTypeLike) -> Array:
  """Copy the array and cast to a specified dtype.

  This is implemented via :func:`jax.lax.convert_element_type`, which may
  have slightly different behavior than :meth:`numpy.ndarray.astype` in
  some cases. In particular, the details of float-to-int and int-to-float
  casts are implementation dependent.
  """
  return lax_numpy.astype(arr, dtype)
