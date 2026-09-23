def _key_data(keys: KeyArray) -> Array:
  assert isinstance(keys, prng.PRNGKeyArray)
  return prng.random_unwrap(keys)
