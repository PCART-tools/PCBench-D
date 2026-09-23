def _key_data(keys: KeyArray) -> Array:
  assert jnp.issubdtype(keys.dtype, dtypes.prng_key)
  return prng.random_unwrap(keys)
