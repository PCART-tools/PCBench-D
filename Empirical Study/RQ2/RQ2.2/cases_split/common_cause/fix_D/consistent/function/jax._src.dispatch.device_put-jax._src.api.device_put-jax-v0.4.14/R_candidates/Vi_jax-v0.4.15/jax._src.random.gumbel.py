def gumbel(key: KeyArray,
           shape: Shape = (),
           dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  """Sample Gumbel random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(x) = e^{-(x + e^{-x})}

  Args:
    key: a PRNG key used as the random key.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified shape and dtype.
  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `gumbel` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.canonicalize_shape(shape)
  return _gumbel(key, shape, dtype)
