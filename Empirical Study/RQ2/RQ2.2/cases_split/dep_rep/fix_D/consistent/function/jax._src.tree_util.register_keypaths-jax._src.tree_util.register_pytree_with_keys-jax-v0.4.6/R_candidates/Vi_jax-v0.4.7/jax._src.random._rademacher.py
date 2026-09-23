@partial(jit, static_argnums=(1, 2), inline=True)
def _rademacher(key, shape, dtype) -> Array:
  bernoulli_samples = bernoulli(key=key, p=0.5, shape=shape).astype(dtype)
  return (2 * bernoulli_samples - 1).astype(dtype)
