@partial(jit, static_argnums=(1,), inline=True)
def _threefry_split_original(key, num) -> jax.Array:
  counts = lax.iota(np.uint32, num * 2)
  return lax.reshape(threefry_2x32(key, counts), (num, 2))
