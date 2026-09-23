@partial(jit, static_argnums=(1, 2), inline=True)
def _cauchy(key, shape, dtype):
  _check_shape("cauchy", shape)
  u = uniform(key, shape, dtype, minval=jnp.finfo(dtype).eps, maxval=1.)
  pi = _lax_const(u, np.pi)
  return lax.tan(lax.mul(pi, lax.sub(u, _lax_const(u, 0.5))))
