@partial(jit, static_argnums=(1, 2))
def _gumbel(key, shape, dtype) -> Array:
  _check_shape("gumbel", shape)
  return -jnp.log(-jnp.log(
      uniform(key, shape, dtype, minval=jnp.finfo(dtype).tiny, maxval=1.)))
