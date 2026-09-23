def ball(
  key: KeyArrayLike,
  d: int,
  p: float = 2,
  shape: Shape = (),
  dtype: DTypeLikeFloat = float
):
  """Sample uniformly from the unit Lp ball.

  Reference: https://arxiv.org/abs/math/0503650.

  Args:
    key: a PRNG key used as the random key.
    d: a nonnegative int representing the dimensionality of the ball.
    p: a float representing the p parameter of the Lp norm.
    shape: optional, the batch dimensions of the result. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array of shape `(*shape, d)` and specified dtype.
  """
  key, _ = _check_prng_key("ball", key)
  dtypes.check_user_dtype_supported(dtype)
  _check_shape("ball", shape)
  d = core.concrete_or_error(index, d, "The error occurred in jax.random.ball()")
  k1, k2 = split(key)
  g = generalized_normal(k1, p, (*shape, d), dtype)
  e = exponential(k2, shape, dtype)
  return g / (((jnp.abs(g) ** p).sum(-1) + e) ** (1 / p))[..., None]
