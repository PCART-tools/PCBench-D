@partial(jit, static_argnums=(4, 5), inline=True)
def _triangular(key, left, mode, right, shape, dtype) -> Array:
  # https://en.wikipedia.org/wiki/Triangular_distribution#Generating_triangular-distributed_random_variates
  if shape is None:
    shape =  lax.broadcast_shapes(np.shape(left), np.shape(mode), np.shape(right))
  else:
    _check_shape("triangular", shape, np.shape(left), np.shape(mode), np.shape(right))
  left = jnp.broadcast_to(left, shape)
  mode = jnp.broadcast_to(mode, shape)
  right = jnp.broadcast_to(right, shape)
  fc = (mode - left) / (right - left)
  u = uniform(key, shape, dtype)
  out1 = left + lax.sqrt(u * (right - left) * (mode - left))
  out2 = right - lax.sqrt((1 - u) * (right - left) * (right - mode))
  tri = lax.select(u < fc, out1, out2)
  return tri
