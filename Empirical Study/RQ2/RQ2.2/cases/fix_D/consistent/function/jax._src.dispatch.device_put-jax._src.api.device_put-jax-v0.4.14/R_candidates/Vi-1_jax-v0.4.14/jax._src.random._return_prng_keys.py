def _return_prng_keys(was_wrapped, key):
  # TODO(frostig): remove once we always enable_custom_prng
  assert jnp.issubdtype(key.dtype, dtypes.prng_key)
  if config.jax_enable_custom_prng:
    return key
  else:
    return prng.random_unwrap(key) if was_wrapped else key
