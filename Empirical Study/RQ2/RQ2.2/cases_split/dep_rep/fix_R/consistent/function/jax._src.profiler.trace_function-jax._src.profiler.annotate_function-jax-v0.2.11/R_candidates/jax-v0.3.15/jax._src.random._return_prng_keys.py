def _return_prng_keys(was_wrapped, key):
  # TODO(frostig): remove once we always enable_custom_prng
  assert type(key) is prng.PRNGKeyArray, type(key)
  if config.jax_enable_custom_prng:
    return key
  else:
    return key.unsafe_raw_array() if was_wrapped else key
