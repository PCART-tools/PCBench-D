def _key_impl(keys: KeyArray) -> PRNGImpl:
  assert jnp.issubdtype(keys.dtype, dtypes.prng_key)
  keys_dtype = typing.cast(prng.KeyTy, keys.dtype)
  return keys_dtype._impl
