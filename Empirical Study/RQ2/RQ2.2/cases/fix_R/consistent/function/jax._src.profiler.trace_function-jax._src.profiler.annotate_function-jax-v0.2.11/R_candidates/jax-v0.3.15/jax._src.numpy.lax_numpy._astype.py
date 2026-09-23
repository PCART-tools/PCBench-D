def _astype(arr, dtype):
  """Copy the array and cast to a specified dtype.

  This is implemeted via :func:`jax.lax.convert_element_type`, which may
  have slightly different behavior than :meth:`numpy.ndarray.astype` in
  some cases. In particular, the details of float-to-int and int-to-float
  casts are implementation dependent.
  """
  if dtype is None:
    dtype = dtypes.canonicalize_dtype(float_)
  lax_internal._check_user_dtype_supported(dtype, "astype")
  return lax.convert_element_type(arr, dtype)
