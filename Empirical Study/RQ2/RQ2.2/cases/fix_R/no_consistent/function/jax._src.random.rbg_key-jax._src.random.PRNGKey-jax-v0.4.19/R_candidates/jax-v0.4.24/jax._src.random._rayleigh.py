@partial(jit, static_argnums=(2, 3))
def _rayleigh(key, scale, shape, dtype) -> Array:
  if shape is None:
    shape = np.shape(scale)
  else:
    _check_shape("rayleigh", shape, np.shape(scale))
  u = uniform(key, shape, dtype)
  scale = scale.astype(dtype)
  scale = jnp.broadcast_to(scale, shape)
  log_u = lax.log(u)
  n_two = _lax_const(scale, -2)
  sqrt_u = lax.sqrt(lax.mul(log_u, n_two))
  ray = lax.mul(scale, sqrt_u)
  return ray
