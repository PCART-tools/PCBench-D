def f(key: KeyArray,
      dfnum: RealArray,
      dfden: RealArray,
      shape: Optional[Shape] = None,
      dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  """Sample F-distribution random values with given shape and float dtype.

  Args:
    key: a PRNG key used as the random key.
    dfnum: a float or array of floats broadcast-compatible with ``shape``
      representing the numerator's ``df`` of the distribution.
    dfden: a float or array of floats broadcast-compatible with ``shape``
      representing the denominator's ``df`` of the distribution.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``dfnum`` and ``dfden``.
      The default (None) produces a result shape equal to ``dfnum.shape``,
      and ``dfden.shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``df.shape``.
  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError("dtype argument to `f` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  return _f(key, dfnum, dfden, shape, dtype)
