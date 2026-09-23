@partial(jit, static_argnums=(2, 3), inline=True)
def _lognormal(key, sigma, shape, dtype) -> Array:
  if shape is None:
    shape =  np.shape(sigma)
  else:
    _check_shape("triangular", shape, np.shape(sigma))
  sigma = jnp.broadcast_to(sigma, shape)
  scaled_norm = normal(key, shape, dtype) * sigma
  return lax.exp(scaled_norm)
