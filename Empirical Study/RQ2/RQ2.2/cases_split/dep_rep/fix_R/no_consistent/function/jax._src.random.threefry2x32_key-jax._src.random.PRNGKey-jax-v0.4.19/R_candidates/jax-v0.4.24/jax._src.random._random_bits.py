def _random_bits(key: KeyArray, bit_width: int, shape: Shape) -> Array:
  assert jnp.issubdtype(key.dtype, dtypes.prng_key)
  return prng.random_bits(key, bit_width=bit_width, shape=shape)
