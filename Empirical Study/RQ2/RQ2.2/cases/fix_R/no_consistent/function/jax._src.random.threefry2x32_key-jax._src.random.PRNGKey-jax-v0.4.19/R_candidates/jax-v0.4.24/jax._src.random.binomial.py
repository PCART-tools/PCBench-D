def binomial(
    key: KeyArray,
    n: RealArray,
    p: RealArray,
    shape: Shape | None = None,
    dtype: DTypeLikeFloat = float,
) -> Array:
  r"""Sample Binomial random values with given shape and float dtype.

  The values are returned according to the probability mass function:

  .. math::
      f(k;n,p) = \binom{n}{k}p^k(1-p)^{n-k}

  on the domain :math:`0 < p < 1`, and where :math:`n` is a nonnegative integer
  representing the number of trials and :math:`p` is a float representing the
  probability of success of an individual trial.

  Args:
    key: a PRNG key used as the random key.
    n: a float or array of floats broadcast-compatible with ``shape``
      representing the number of trials.
    p: a float or array of floats broadcast-compatible with ``shape``
      representing the probability of success of an individual trial.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``n`` and ``p``.
      The default (None) produces a result shape equal to ``np.broadcast(n, p).shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified dtype and with shape given by
    ``np.broadcast(n, p).shape``.
  """
  key, _ = _check_prng_key("binomial", key)
  check_arraylike("binomial", n, p)
  dtypes.check_user_dtype_supported(dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(
        "dtype argument to `binomial` must be a float dtype, got {dtype}"
      )
  dtype = dtypes.canonicalize_dtype(dtype)
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  return _binomial(key, n, p, shape, dtype)
