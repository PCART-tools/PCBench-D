@partial(jit, static_argnums=(2, 3), inline=True)
def _wald(key, mean, shape, dtype) -> Array:
  if shape is None:
    shape =  np.shape(mean)
  else:
    _check_shape("wald", shape, np.shape(mean))
  k1, k2 = _split(key, 2)
  mean = mean.astype(dtype)
  mean = jnp.broadcast_to(mean, shape)
  v = normal(k1, shape, dtype)
  z = uniform(k2, shape, dtype)
  y = lax.integer_pow(v, 2)
  y_sq = lax.integer_pow(y, 2)
  mean_sq = lax.integer_pow(mean, 2)
  sqrt_term = lax.sqrt(4 * mean * y + mean_sq * y_sq)
  x = mean + mean_sq * y / 2 - mean / 2 * sqrt_term
  w = lax.select(lax.le(z,  mean / (mean + x)), x, mean_sq / x)
  return w
