def normal(key: KeyArray,
           shape: Union[Shape, NamedShape] = (),
           dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  """Sample standard normal random values with given shape and float dtype.

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
  if not dtypes.issubdtype(dtype, np.inexact):
    raise ValueError(f"dtype argument to `normal` must be a float or complex dtype, "
                     f"got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.as_named_shape(shape)
  return _normal(key, shape, dtype)  # type: ignore
