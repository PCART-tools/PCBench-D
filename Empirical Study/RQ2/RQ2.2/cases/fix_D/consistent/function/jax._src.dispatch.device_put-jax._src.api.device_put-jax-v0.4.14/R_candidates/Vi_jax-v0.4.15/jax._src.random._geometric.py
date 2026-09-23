@partial(jit, static_argnums=(2, 3))
def _geometric(key, p, shape, dtype) -> Array:
  if shape is None:
    shape =  np.shape(p)
  else:
    _check_shape("geometric", shape, np.shape(p))
  check_arraylike("geometric", p)
  p, = promote_dtypes_inexact(p)
  u = uniform(key, shape, p.dtype)
  log_u = lax.log(u)
  log_one_minus_p = lax.log1p(-p)
  log_one_minus_p = jnp.broadcast_to(log_one_minus_p, shape)
  g = lax.floor(lax.div(log_u, log_one_minus_p)) + 1
  return g.astype(dtype)
