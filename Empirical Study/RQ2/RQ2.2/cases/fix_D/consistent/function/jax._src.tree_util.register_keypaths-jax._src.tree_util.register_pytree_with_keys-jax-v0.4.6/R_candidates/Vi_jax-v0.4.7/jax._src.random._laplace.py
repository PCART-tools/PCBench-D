@partial(jit, static_argnums=(1, 2), inline=True)
def _laplace(key, shape, dtype) -> Array:
  _check_shape("laplace", shape)
  u = uniform(
      key, shape, dtype, minval=-1. + jnp.finfo(dtype).epsneg, maxval=1.)
  return lax.mul(lax.sign(u), lax.log1p(lax.neg(lax.abs(u))))
