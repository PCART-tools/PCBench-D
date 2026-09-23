def _random_bits(key: prng.PRNGKeyArray, bit_width, shape) -> Array:
  assert jnp.issubdtype(key.dtype, dtypes.prng_key)
  return prng.random_bits(key, bit_width=bit_width, shape=shape)
