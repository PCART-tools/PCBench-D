def _random_bits(key: prng.PRNGKeyArray, bit_width, shape) -> jnp.ndarray:
  key, _ = _check_prng_key(key)
  return key._random_bits(bit_width, shape)
