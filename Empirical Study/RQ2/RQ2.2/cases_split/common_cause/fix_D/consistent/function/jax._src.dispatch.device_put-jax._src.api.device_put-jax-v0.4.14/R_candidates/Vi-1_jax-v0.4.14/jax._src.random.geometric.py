def geometric(key: KeyArray,
              p: RealArray,
              shape: Optional[Shape] = None,
              dtype: DTypeLikeInt = dtypes.int_) -> Array:
  r"""Sample Geometric random values with given shape and float dtype.

  The values are returned according to the probability mass function:

  .. math::
      f(k;p) = p(1-p)^{k-1}

  on the domain :math:`0 < p < 1`.

  Args:
    key: a PRNG key used as the random key.
    p: a float or array of floats broadcast-compatible with ``shape``
      representing the the probability of success of an individual trial.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``p``. The default
      (None) produces a result shape equal to ``np.shape(p)``.
    dtype: optional, a int dtype for the returned values (default int64 if
      jax_enable_x64 is true, otherwise int32).

  Returns:
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``p.shape``.
  """
  key, _ = _check_prng_key(key)
  if not dtypes.issubdtype(dtype, np.integer):
    raise ValueError("dtype argument to `geometric` must be an int "
                     f"dtype, got {dtype}")
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  return _geometric(key, p, shape, dtype)
