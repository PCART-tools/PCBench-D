def key_data(keys: KeyArray) -> Array:
  keys, _ = _check_prng_key(keys)
  return _key_data(keys)
