def lognormal(key: KeyArray,
              sigma: RealArray = np.float32(1),
              shape: Optional[Shape] = None,
              dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  r""" Sample lognormal random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
      f(x) = \frac{1}{x\sqrt{2\pi\sigma^2}}\exp\left(-\frac{(\log x)^2}{2\sigma^2}\right)

  on the domain :math:`x > 0`.

  Args:
    key: a PRNG key used as the random key.
    sigma: a float or array of floats broadcast-compatible with ``shape`` representing
      the standard deviation of the underlying normal distribution. Default 1.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. The default (None) produces a result shape equal to ``()``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified dtype and with shape given by ``shape``.
  """
  key, _ = _check_prng_key(key)
  dtypes.check_user_dtype_supported(dtype)
  if not dtypes.issubdtype(dtype, np.inexact):
    raise ValueError(f"dtype argument to `lognormal` must be a float or complex dtype, "
                     f"got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  return _lognormal(key, sigma, shape, dtype)  # type: ignore
