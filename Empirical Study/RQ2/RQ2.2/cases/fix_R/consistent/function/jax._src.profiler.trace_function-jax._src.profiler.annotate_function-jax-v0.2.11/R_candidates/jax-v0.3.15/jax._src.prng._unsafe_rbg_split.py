def _unsafe_rbg_split(key: jnp.ndarray, num: int) -> jnp.ndarray:
  # treat 10 iterations of random bits as a 'hash function'
  _, keys = lax.rng_bit_generator(key, (10 * num, 4), dtype='uint32')
  return keys[::10]
