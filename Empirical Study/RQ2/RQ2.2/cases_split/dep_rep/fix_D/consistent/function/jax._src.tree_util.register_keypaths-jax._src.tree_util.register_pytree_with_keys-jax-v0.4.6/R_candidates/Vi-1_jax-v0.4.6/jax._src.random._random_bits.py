def _random_bits(key: prng.PRNGKeyArray, bit_width, shape) -> Array:
  assert isinstance(key, prng.PRNGKeyArray)
  return prng.random_bits(key, bit_width=bit_width, shape=shape)
