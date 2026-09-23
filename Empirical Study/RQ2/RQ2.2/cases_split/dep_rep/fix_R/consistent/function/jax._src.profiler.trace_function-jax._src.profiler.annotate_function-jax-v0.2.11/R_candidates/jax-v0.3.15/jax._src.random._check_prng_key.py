def _check_prng_key(key):
  # TODO(frostig): remove once we always enable_custom_prng
  if type(key) is prng.PRNGKeyArray:
    return key, False
  elif _arraylike(key):
    if config.jax_enable_custom_prng:
      warnings.warn(
          'Raw arrays as random keys to jax.random functions are deprecated. '
          'Assuming valid threefry2x32 key for now.',
          FutureWarning)
    return prng.PRNGKeyArray(default_prng_impl(), key), True
  else:
    raise TypeError(f'unexpected PRNG key type {type(key)}')
