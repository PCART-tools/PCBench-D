def t(key: KeyArray,
      df: RealArray,
      shape: Shape = (),
      dtype: DTypeLikeFloat = dtypes.float_) -> Array:
  r"""Sample Student's t random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(t; \nu) \propto \left(1 + \frac{t^2}{\nu}\right)^{-(\nu + 1)/2}

  Where :math:`\nu > 0` is the degrees of freedom, given by the parameter ``df``.

  Args:
    key: a PRNG key used as the random key.
    df: a float or array of floats broadcast-compatible with ``shape``
      representing the degrees of freedom parameter of the distribution.
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
    raise ValueError(f"dtype argument to `t` must be a float "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.canonicalize_shape(shape)
  return _t(key, df, shape, dtype)
