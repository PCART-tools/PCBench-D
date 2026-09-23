def chisquare(key: KeyArray,
              df: RealArray,
              shape: Optional[Shape] = None,
              dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  r"""Sample Chisquare random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(x; \nu) \propto x^{k/2 - 1}e^{-x/2}

  on the domain :math:`0 < x < \infty`, where :math:`\nu > 0` represents the
  degrees of freedom, given by the parameter ``df``.

  Args:
    key: a PRNG key used as the random key.
    df: a float or array of floats broadcast-compatible with ``shape``
      representing the parameter of the distribution.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``df``. The default (None)
      produces a result shape equal to ``df.shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``df.shape``.
  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError("dtype argument to `chisquare` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  return _chisquare(key, df, shape, dtype)
