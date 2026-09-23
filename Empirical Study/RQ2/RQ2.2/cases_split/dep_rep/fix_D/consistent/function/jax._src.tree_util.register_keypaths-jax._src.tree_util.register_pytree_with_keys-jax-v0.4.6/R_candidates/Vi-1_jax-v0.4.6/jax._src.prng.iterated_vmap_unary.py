def iterated_vmap_unary(n, f):
  for _ in range(n):
    f = jax.vmap(f)
  return f
