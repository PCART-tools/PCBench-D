def generalized_normal(
  key: KeyArray,
  p: float,
  shape: Shape = (),
  dtype: DTypeLikeFloat = dtypes.float_
) -> Array:
  """Sample from the generalized normal distribution.

  Args:
    key: a PRNG key used as the random key.
    p: a float representing the shape parameter.
    shape: optional, the batch dimensions of the result. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array with the specified shape and dtype.
  """
  key, _ = _check_prng_key(key)
  _check_shape("generalized_normal", shape)
  keys = split(key)
  g = gamma(keys[0], 1/p, shape, dtype)
  r = rademacher(keys[1], shape, dtype)
  return r * g ** (1 / p)
