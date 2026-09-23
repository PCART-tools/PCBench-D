def normal(key: KeyArrayLike,
           shape: Shape | NamedShape = (),
           dtype: DTypeLikeFloat = float) -> Array:
  r"""Sample standard normal random values with given shape and float dtype.

  The values are returned according to the probability density function:

  .. math::
     f(x) = \frac{1}{\sqrt{2\pi}}e^{-x^2/2}

  on the domain :math:`-\infty < x < \infty`

  Args:
    key: a PRNG key used as the random key.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified shape and dtype.
  """
  key, _ = _check_prng_key("normal", key)
  dtypes.check_user_dtype_supported(dtype)
  if not dtypes.issubdtype(dtype, np.inexact):
    raise ValueError(f"dtype argument to `normal` must be a float or complex dtype, "
                     f"got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.as_named_shape(shape)
  return _normal(key, shape, dtype)  # type: ignore
