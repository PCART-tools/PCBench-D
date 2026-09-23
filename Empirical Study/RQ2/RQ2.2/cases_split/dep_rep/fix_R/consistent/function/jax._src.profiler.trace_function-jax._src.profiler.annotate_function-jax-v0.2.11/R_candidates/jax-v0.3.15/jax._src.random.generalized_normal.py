def generalized_normal(
  key: KeyArray,
  p: float,
  shape: Sequence[int] = (),
  dtype: DTypeLikeFloat = dtypes.float_
) -> jnp.ndarray:
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
  _check_shape("generalized_normal", shape)
  keys = split(key)
  g = gamma(keys[0], 1/p, shape, dtype)
  r = rademacher(keys[1], shape, dtype)
  return r * g ** (1 / p)
