@partial(jit, static_argnums=(1, 2))
def _maxwell(key, shape, dtype) -> Array:
  shape = shape + (3,)
  norm_rvs = normal(key=key, shape=shape, dtype=dtype)
  return jnp.linalg.norm(norm_rvs, axis=-1)
