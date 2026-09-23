@partial(jit, static_argnums=(1, 2))
def _logistic(key, shape, dtype):
  _check_shape("logistic", shape)
  x = uniform(key, shape, dtype, minval=jnp.finfo(dtype).eps, maxval=1.)
  return lax.log(lax.div(x, lax.sub(_lax_const(x, 1), x)))
