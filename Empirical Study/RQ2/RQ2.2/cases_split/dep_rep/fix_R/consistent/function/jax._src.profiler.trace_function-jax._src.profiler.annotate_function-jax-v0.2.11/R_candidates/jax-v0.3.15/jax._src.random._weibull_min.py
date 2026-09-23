@partial(jit, static_argnums=(3, 4), inline=True)
def _weibull_min(key, scale, concentration, shape, dtype):
  random_uniform = uniform(
      key=key, shape=shape, minval=0, maxval=1, dtype=dtype)

  # Inverse weibull CDF.
  return jnp.power(-jnp.log1p(-random_uniform), 1.0/concentration) * scale
