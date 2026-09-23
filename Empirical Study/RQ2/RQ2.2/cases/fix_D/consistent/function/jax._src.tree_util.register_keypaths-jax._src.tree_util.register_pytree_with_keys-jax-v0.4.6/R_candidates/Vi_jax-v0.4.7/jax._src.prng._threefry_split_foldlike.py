@partial(jit, static_argnums=(1,), inline=True)
def _threefry_split_foldlike(key, num) -> jax.Array:
  k1, k2 = key
  counts1, counts2 = iota_2x32_shape((num,))
  bits1, bits2 = threefry2x32_p.bind(k1, k2, counts1, counts2)
  return jnp.stack([bits1, bits2], axis=1)
